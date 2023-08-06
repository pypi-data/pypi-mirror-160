

Example Project
===============
This project aims to implement the most basic modules to produce a language model.

Installing
============

.. code-block:: bash

    pip install binh-language-model

Usage
=====

.. code-block:: bash

    from bert.modeling_bert import BertModel
    from bert.configuration_bert import BertConfig

    config = BertConfig()
    import torch
    inputs_ids = torch.tensor([[1,2,3,4]])
    attention_mask = torch.tensor([[1,1,1,0]])
    token_type_ids = torch.tensor([[1,1,1,1]])
    model = BertModel(config)
    outputs = model(inputs_ids, attention_mask, token_type_ids)