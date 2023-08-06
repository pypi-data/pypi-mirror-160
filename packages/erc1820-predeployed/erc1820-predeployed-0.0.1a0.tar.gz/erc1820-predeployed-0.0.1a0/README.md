# erc1820-predeployed

## Description

A tool for generating predeployed ERC1820Registry smart contract

## Installation

```console
pip install erc1820-predeployed
```

## Usage example

```python
from erc1820_predeployed import  ERC1820RegistryGenerator, ERC1820_REGISTRY_ADDRESS

erc1820_registry_generator = ERC1820RegistryGenerator()

genesis = {
    # genesis block parameters
    'alloc': {
        **erc1820_registry_generator.generate_allocation(
            contract_address=ERC1820_REGISTRY_ADDRESS
        )
    }
}

```