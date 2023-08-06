#!/usr/bin/env python
# coding=utf-8

import torch
import torch.nn as nn
from torch.nn import Module, Parameter, Embedding, Linear, MaxPool1d, AvgPool1d, Dropout, LSTM
from torch.nn.init import kaiming_normal_
import torch.nn.functional as F
import numpy as np
import datetime
# from models.utils import RobertaEncode


device = "cpu" if not torch.cuda.is_available() else "cuda"
# print(f"device:{device}")

class DKVMNHeadGroup(nn.Module):
    def forward(self, input_):
        pass

    def __init__(self, memory_size, memory_state_dim, is_write):
        super(DKVMNHeadGroup, self).__init__()
        """"
        Parameters
            memory_size:        scalar
            memory_state_dim:   scalar
            is_write:           boolean
        """
        self.memory_size = memory_size
        self.memory_state_dim = memory_state_dim
        self.is_write = is_write
        if self.is_write:
            self.erase = torch.nn.Linear(self.memory_state_dim, self.memory_state_dim, bias=True)
            self.add = torch.nn.Linear(self.memory_state_dim, self.memory_state_dim, bias=True)
            nn.init.kaiming_normal_(self.erase.weight)
            nn.init.kaiming_normal_(self.add.weight)
            nn.init.constant_(self.erase.bias, 0)
            nn.init.constant_(self.add.bias, 0)

    @staticmethod
    def addressing(control_input, memory):
        """
        Parameters
            control_input:          Shape (batch_size, control_state_dim)
            memory:                 Shape (memory_size, memory_state_dim)
        Returns
            correlation_weight:     Shape (batch_size, memory_size)
        """
        similarity_score = torch.matmul(control_input, torch.t(memory))  # torch.t做转置
        correlation_weight = F.softmax(similarity_score, dim=1)  # Shape: (batch_size, memory_size)
        return correlation_weight

    ## Read Process By Sum Memory By Read_Weight
    def read(self, memory, control_input=None, read_weight=None):
        """
        Parameters
            control_input:  Shape (batch_size, control_state_dim)
            memory:         Shape (batch_size, memory_size, memory_state_dim)
            read_weight:    Shape (batch_size, memory_size)
        Returns
            read_content:   Shape (batch_size,  memory_state_dim)
        """
        if read_weight is None:
            read_weight = self.addressing(control_input=control_input, memory=memory)
        read_weight = read_weight.view(-1, 1)  # 列tensor
        memory = memory.view(-1, self.memory_state_dim)
        rc = torch.mul(read_weight, memory)  # 矩阵对应位相乘，两者维度要相等
        read_content = rc.view(-1, self.memory_size, self.memory_state_dim)
        read_content = torch.sum(read_content, dim=1)
        return read_content

    def write(self, control_input, memory, write_weight=None):
        """
        Parameters
            control_input:      Shape (batch_size, control_state_dim)
            write_weight:       Shape (batch_size, memory_size)
            memory:             Shape (batch_size, memory_size, memory_state_dim)
        Returns
            new_memory:         Shape (batch_size, memory_size, memory_state_dim)
        """
        assert self.is_write
        if write_weight is None:
            write_weight = self.addressing(control_input=control_input, memory=memory)
        erase_signal = torch.sigmoid(self.erase(control_input))
        # print(f"erase_signal: {erase_signal.shape}")
        add_signal = torch.tanh(self.add(control_input))
        # print(f"add_signal: {add_signal.shape}")
        erase_reshape = erase_signal.view(-1, 1, self.memory_state_dim)
        # print(f"erase_reshape: {erase_reshape.shape}")
        add_reshape = add_signal.view(-1, 1, self.memory_state_dim)
        # print(f"add_reshape : {add_reshape .shape}")
        write_weight_reshape = write_weight.view(-1, self.memory_size, 1)
        # print(f"write_weight_reshape: {write_weight_reshape.shape}")
        erase_mul = torch.mul(erase_reshape, write_weight_reshape)
        # print(f"erase_mul: {erase_mul.shape}")
        add_mul = torch.mul(add_reshape, write_weight_reshape)
        # print(f"add_mul: {add_mul.shape}")
        memory = memory.to(device)
        # print(f"memory: {memory.shape}")
        if add_mul.shape[0] < memory.shape[0]:
            sub_memory = memory[:add_mul.shape[0],:,:]
            new_memory = torch.cat([sub_memory * (1 - erase_mul) + add_mul, memory[add_mul.shape[0]:,:,:]], dim=0)
        else:
            new_memory = memory * (1 - erase_mul) + add_mul
        return new_memory


class DKVMN(nn.Module):
    def forward(self, input_):
        pass

    def __init__(self, memory_size, memory_key_state_dim, memory_value_state_dim, init_memory_key, memory_value=None):
        super(DKVMN, self).__init__()
        """
        :param memory_size:             scalar
        :param memory_key_state_dim:    scalar
        :param memory_value_state_dim:  scalar
        :param init_memory_key:         Shape (memory_size, memory_value_state_dim)
        """
        self.memory_size = memory_size
        self.memory_key_state_dim = memory_key_state_dim
        self.memory_value_state_dim = memory_value_state_dim

        self.key_head = DKVMNHeadGroup(memory_size=self.memory_size,
                                       memory_state_dim=self.memory_key_state_dim,
                                       is_write=False)
        self.value_head = DKVMNHeadGroup(memory_size=self.memory_size,
                                         memory_state_dim=self.memory_value_state_dim,
                                         is_write=True)

        self.memory_key = init_memory_key


    def attention(self, control_input):
        correlation_weight = self.key_head.addressing(control_input=control_input, memory=self.memory_key)
        return correlation_weight

    def read(self, read_weight, memory_value):
        read_content = self.value_head.read(memory=memory_value, read_weight=read_weight)

        return read_content

    def write(self, write_weight, control_input, memory_value):
        memory_value = self.value_head.write(control_input=control_input,
                                             memory=memory_value,
                                             write_weight=write_weight)

        return memory_value


class SKVMN(Module):
    def __init__(self, num_c, dim_s, size_m, dropout=0.2, emb_type="qid", emb_path="", use_onehot=True):
        super().__init__()
        self.model_name = "skvmn"
        self.num_c = num_c
        self.dim_s = dim_s
        self.size_m = size_m
        self.emb_type = emb_type
        self.use_onehot = use_onehot

        if emb_type.startswith("qid"):
            self.k_emb_layer = Embedding(self.num_c, self.dim_s)
            self.Mk = Parameter(torch.Tensor(self.size_m, self.dim_s))
            self.Mv0 = Parameter(torch.Tensor(self.size_m, self.dim_s))

        kaiming_normal_(self.Mk)
        kaiming_normal_(self.Mv0)

        self.mem = DKVMN(memory_size=size_m,
           memory_key_state_dim=dim_s,
           memory_value_state_dim=dim_s, init_memory_key=self.Mk)
                
        self.a_embed = nn.Linear(self.dim_s, self.dim_s, bias=True)
        # self.a_embed = nn.Linear(self.num_c + self.dim_s*2, self.dim_s, bias=True)
        self.v_emb_layer = Embedding(self.dim_s * 2, self.dim_s)
        self.f_layer = Linear(self.dim_s * 2, self.dim_s)
        self.hx = Parameter(torch.Tensor(1, self.dim_s))
        self.cx = Parameter(torch.Tensor(1, self.dim_s))
        kaiming_normal_(self.hx)
        kaiming_normal_(self.cx)
        self.dropout_layer = Dropout(dropout)
        self.p_layer = Linear(self.dim_s, 1)
        self.lstm_cell = nn.LSTMCell(self.dim_s, self.dim_s)

    def ut_mask(self, seq_len):
        return torch.triu(torch.ones(seq_len, seq_len), diagonal=0).to(dtype=torch.bool)

    def forward(self, q, r):
        emb_type = self.emb_type
        bs = q.shape[0]              
        self.seqlen = q.shape[1]

        if emb_type == "qid":
            x = q + self.num_c * r
            k = self.k_emb_layer(q)#[bs, seqlen, dim_s]
            v = self.v_emb_layer(x)#[bs, seqlen, dim_s]

        Mvt = self.Mv0.unsqueeze(0).repeat(bs, 1, 1).to(device) #[bs, size_m, dim_s]

        w = torch.softmax(torch.matmul(k, self.mem.memory_key.T), dim=-1)#[bs, seqlen, size_m]
        print(f"k : {k.shape},w : {w.shape},")

        Mv = [Mvt]
        for i in range(self.seqlen):
            q = k.permute(1,0,2)[i]
            # write_embed = torch.cat([q, v[:,:,i]], -1) # bz * 2dim_s
            write_embed = v.permute(1,0,2)[i] # dim_s
            # print(f"write_embeds shape is {write_embed.shape}")
            write_embed = self.a_embed(write_embed).to(device) #[bs, dim_s]
            # print(f"write_embed: {write_embed}")
            correlation_weight = w.permute(1,0,2)[i]
            Mvt = self.mem.write(correlation_weight, write_embed, Mvt)
            Mv.append(Mvt)


        Mv = torch.stack(Mv, dim=1)
        f = torch.tanh(
            self.f_layer(
                torch.cat(
                    [
                        (w.unsqueeze(-1) * Mv[:, :-1]).sum(-2),
                        k
                    ],
                    dim=-1
                )
            )
        )
        p = self.p_layer(self.dropout_layer(f))
        p = torch.sigmoid(p)
        p = p.squeeze(-1)

        return p

