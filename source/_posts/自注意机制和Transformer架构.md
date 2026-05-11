---
title: 自注意机制和Transformer架构
date: 2026-01-24 16:27:39
tags:
  - 深度学习
---

## Word Embedding  

![image-20260124163317586](自注意机制和Transformer架构/image-20260124163317586.png)

Word Embedding 会给每一个词汇一个向量, 而一个句子就是一排长度不一的向量

声音信号也是一堆向量

![image-20260124163739911](自注意机制和Transformer架构/image-20260124163739911.png)

一个分子也可以看做一个graph

## 三种可能输出

![image-20260124164422324](自注意机制和Transformer架构/image-20260124164422324.png)

## Sequence Labeling

第一种输出也叫 Sequence Labeling

FC: Fully-connected network

![image-20260124164954595](自注意机制和Transformer架构/image-20260124164954595.png)

## Self-attention



![image-20260124165317713](自注意机制和Transformer架构/image-20260124165317713.png)





self-attention 可以叠加很多次

![image-20260124172926459](自注意机制和Transformer架构/image-20260124172926459.png)





![image-20260124175402401](自注意机制和Transformer架构/image-20260124175402401.png)

计算α的方法有很多种

![image-20260124173353167](自注意机制和Transformer架构/image-20260124173353167.png)

一般采用Dot-product 去计算 attention score

![image-20260124175908821](自注意机制和Transformer架构/image-20260124175908821.png)

由a怎么得到的qkv

![image-20260125164714270](自注意机制和Transformer架构/image-20260125164714270.png)

![image-20260125173013085](自注意机制和Transformer架构/image-20260125173013085.png)



![image-20260125173025239](自注意机制和Transformer架构/image-20260125173025239.png)
