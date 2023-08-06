from web3.auto import w3

from erc1820_predeployed import ERC1820RegistryGenerator, ERC1820_REGISTRY_ADDRESS
from .tools.test_solidity_project import TestSolidityProject


class TestERC1820RegistryGenerator(TestSolidityProject):

    def get_multisig_abi(self):
        return self.get_abi('ERC1820Registry')

    def test_meta_info(self):
        meta = ERC1820RegistryGenerator().get_meta()
        assert meta['name'] == 'ERC1820Registry'
    