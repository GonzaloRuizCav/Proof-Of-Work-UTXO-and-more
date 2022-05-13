from blockchain.block import Block
from blockchain import util
import config
import binascii
import ecdsa
from ecdsa import SigningKey, VerifyingKey

class PoABlock(Block):
    """ Extends Block, adding proof-of-work primitives. """

    def seal_is_valid(self):
        """ Checks whether a block's seal_data forms a valid seal.
            In PoA, this means that Verif(PK, [block, sig]) = accept.
            (aka the unsealed block header is validly signed under the authority's public key)

            Returns:
                bool: True only if a block's seal data forms a valid seal according to PoA.
        """
        if self.seal_data == 0:
            return False

        # Decode signature to bytes, verify it
        signature = hex(self.seal_data)[2:].zfill(96)
        return util.is_message_signed(self.unsealed_header(), signature, config.AUTHORITY_PK)

    def get_weight(self):
        """ All blocks have same weight in PoA """
        return 1

    def mine(self):
        """ PoA signer; seals a block with new seal data by signing it, checking that
            signature is valid, and returning.
        """
        while True:
            Encoded_header = self.unsealed_header().encode("utf-8")
            private_key = self.get_private_key()
            sk = SigningKey.from_string(private_key, curve = ecdsa.NIST192p)
            result = sk.sign(Encoded_header)
            self.set_seal_data(int.from_bytes(result, 'big'))
            if self.seal_is_valid():
                break
        return

    def calculate_appropriate_target(self):
        """ Target in PoA is currently meaningless """
        return 0

