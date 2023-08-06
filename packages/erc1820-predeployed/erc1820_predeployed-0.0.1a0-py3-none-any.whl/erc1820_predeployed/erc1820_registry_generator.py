'''Module for generation of ERC1820Registry predeployed smart contract'''

from os.path import dirname, join
from typing import Dict

from predeployed_generator.contract_generator import ContractGenerator


class ERC1820RegistryGenerator(ContractGenerator):
    '''Generates ERC1820Registry
    '''

    ARTIFACT_FILENAME = 'ERC1820Registry.json'
    META_FILENAME = 'ERC1820Registry.meta.json'

    # ---------- storage ----------
    # ------ ERC1820Registry ------

    def __init__(self):
        generator = ERC1820RegistryGenerator.from_hardhat_artifact(
            join(dirname(__file__), 'artifacts', self.ARTIFACT_FILENAME),
            join(dirname(__file__), 'artifacts', self.META_FILENAME))
        super().__init__(bytecode=generator.bytecode, abi=generator.abi, meta=generator.meta)

    @classmethod
    def generate_storage(cls, **_) -> Dict[str, str]:
        '''Generate contract storage
        '''
        storage: Dict[str, str] = {}
        return storage
