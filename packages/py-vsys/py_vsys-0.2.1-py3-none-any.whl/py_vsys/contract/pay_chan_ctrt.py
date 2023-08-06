"""
pay_chan_ctrt contains Payment Channel contract.
"""
from __future__ import annotations
import struct
from typing import TYPE_CHECKING, Dict, Any, Union, Optional

import base58
from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_vsys import account as acnt
    from py_vsys import chain as ch

from py_vsys import data_entry as de
from py_vsys import tx_req as tx
from py_vsys import model as md
from py_vsys.contract import tok_ctrt_factory as tcf
from py_vsys.utils.crypto import curve_25519 as curve
from . import Ctrt, BaseTokCtrt


class PayChanCtrt(Ctrt):
    """
    PayChanCtrt is the class for VSYS Payment Channel contract.
    """

    CTRT_META = md.CtrtMeta.from_b58_str(
        "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"
    )

    class FuncIdx(Ctrt.FuncIdx):
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        CREATE_AND_LOAD = 0
        EXTEND_EXPIRATION_TIME = 1
        LOAD = 2
        ABORT = 3
        UNLOAD = 4
        COLLECT_PAYMENT = 5

    class StateVar(Ctrt.StateVar):
        """
        StateVar is the enum class for state variables of a contract.
        """

        MAKER = 0
        TOKEN_ID = 1

    class StateMapIdx(Ctrt.StateMapIdx):
        """
        StateMapIdx is the enum class for state map indexes.
        """

        CONTRACT_BALANCE = 0
        CHANNEL_CREATOR = 1
        CHANNEL_CREATOR_PUBLIC_KEY = 2
        CHANNEL_RECIPIENT = 3
        CHANNEL_ACCUMULATED_LOAD = 4
        CHANNEL_ACCUMULATED_PAYMENT = 5
        CHANNEL_EXPIRATION_TIME = 6
        CHANNEL_STATUS = 7

    class DBKey(Ctrt.DBKey):
        """
        DBKey is the class for DB key of a contract used to query data.
        """

        @classmethod
        def for_maker(cls) -> PayChanCtrt.DBKey:
            """
            for_maker returns the PayChanCtrt.DBKey object for querying the maker.

            Returns:
                PayChanCtrt.DBKey: The PayChanCtrt.DBKey object.
            """
            b = PayChanCtrt.StateVar.MAKER.serialize()
            return cls(b)

        @classmethod
        def for_token_id(cls) -> PayChanCtrt.DBKey:
            """
            for_token_id returns the PayChanCtrt.DBKey object for querying the token_id.

            Returns:
                PayChanCtrt.DBKey: The PayChanCtrt.DBKey object.
            """
            b = PayChanCtrt.StateVar.TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_contract_balance(cls, addr: str) -> PayChanCtrt.DBKey:
            """
            for_contract_balance returns the PayChanCtrt.DBKey object for querying the contract balance.

            Args:
                addr (str): The account address.

            Returns:
                PayChanCtrt.DBKey: The PayChanCtrt.DBKey object.
            """
            b = PayChanCtrt.StateMap(
                idx=PayChanCtrt.StateMapIdx.CONTRACT_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_channel_creator(cls, chan_id: str) -> PayChanCtrt.DBKey:
            """
            for_channel_creator returns the PayChanCtrt.DBKey object for querying the channel creator.

            Args:
                chan_id (str): The channel ID.

            Returns:
                PayChanCtrt.DBKey: The PayChanCtrt.DBKey object.
            """
            b = PayChanCtrt.StateMap(
                idx=PayChanCtrt.StateMapIdx.CHANNEL_CREATOR,
                data_entry=de.Bytes.from_base58_str(chan_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_channel_creator_public_key(cls, chan_id: str) -> PayChanCtrt.DBKey:
            """
            for_channel_creator_public_key returns the PayChanCtrt.DBKey object for querying the public key
            of the channel creator.

            Args:
                chan_id (str): The channel ID.

            Returns:
                PayChanCtrt.DBKey: The PayChanCtrt.DBKey object.
            """
            b = PayChanCtrt.StateMap(
                idx=PayChanCtrt.StateMapIdx.CHANNEL_CREATOR_PUBLIC_KEY,
                data_entry=de.Bytes.from_base58_str(chan_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_channel_recipient(cls, chan_id: str) -> PayChanCtrt.DBKey:
            """
            for_channel_recipient returns the PayChanCtrt.DBKey object for querying the channel recipient.

            Args:
                chan_id (str): The channel ID.

            Returns:
                PayChanCtrt.DBKey: The PayChanCtrt.DBKey object.
            """
            b = PayChanCtrt.StateMap(
                idx=PayChanCtrt.StateMapIdx.CHANNEL_RECIPIENT,
                data_entry=de.Bytes.from_base58_str(chan_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_channel_accumulated_load(cls, chan_id: str) -> PayChanCtrt.DBKey:
            """
            for_channel_accumulated_load returns the PayChanCtrt.DBKey object for querying the
            accumulated amount loaded into the channel.

            Args:
                chan_id (str): The channel ID.

            Returns:
                PayChanCtrt.DBKey: The PayChanCtrt.DBKey object.
            """
            b = PayChanCtrt.StateMap(
                idx=PayChanCtrt.StateMapIdx.CHANNEL_ACCUMULATED_LOAD,
                data_entry=de.Bytes.from_base58_str(chan_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_channel_accumulated_payment(cls, chan_id: str) -> PayChanCtrt.DBKey:
            """
            for_channel_accumulated returns the PayChanCtrt.DBKey object for querying the
            accumulated amount already collected by the recipient.

            Args:
                chan_id (str): The channel ID.

            Returns:
                PayChanCtrt.DBKey: The PayChanCtrt.DBKey object.
            """
            b = PayChanCtrt.StateMap(
                idx=PayChanCtrt.StateMapIdx.CHANNEL_ACCUMULATED_PAYMENT,
                data_entry=de.Bytes.from_base58_str(chan_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_channel_expiration_time(cls, chan_id: str) -> PayChanCtrt.DBKey:
            """
            for_channel_expiration_time returns the PayChanCtrt.DBKey object for querying the
            expiration time of the channel, after which the creator can unload the funds.

            Args:
                chan_id (str): The channel ID.

            Returns:
                PayChanCtrt.DBKey: The PayChanCtrt.DBKey object.
            """
            b = PayChanCtrt.StateMap(
                idx=PayChanCtrt.StateMapIdx.CHANNEL_EXPIRATION_TIME,
                data_entry=de.Bytes.from_base58_str(chan_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_channel_status(cls, chan_id: str) -> PayChanCtrt.DBKey:
            """
            for_channel_status returns the PayChanCtrt.DBKey object for querying the
            expiration time of the channel, after which the creator can unload the funds.

            Args:
                chan_id (str): The channel ID.

            Returns:
                PayChanCtrt.DBKey: The PayChanCtrt.DBKey object.
            """
            b = PayChanCtrt.StateMap(
                idx=PayChanCtrt.StateMapIdx.CHANNEL_STATUS,
                data_entry=de.Bytes.from_base58_str(chan_id),
            ).serialize()
            return cls(b)

    def __init__(self, ctrt_id: str, chain: ch.Chain) -> None:
        """
        Args:
            ctrt_id (str): The id of the contract.
            chain (ch.Chain): The object of the chain where the contract is on.
        """
        super().__init__(ctrt_id, chain)
        self._tok_id: Optional[md.TokenID] = None
        self._tok_ctrt: Optional[BaseTokCtrt] = None

    @property
    async def maker(self) -> md.Addr:
        """
        maker queries & returns the maker of the contract.

        Returns:
            md.Addr: The address of the maker of the contract.
        """
        raw_val = await self._query_db_key(self.DBKey.for_maker())
        return md.Addr(raw_val)

    @property
    async def tok_id(self) -> md.TokenID:
        """
        tok_id queries & returns the token_id of the contract.

        Returns:
            md.TokenID: The token_id of the contract.
        """
        if not self._tok_id:
            raw_val = await self._query_db_key(self.DBKey.for_token_id())
            self._tok_id = md.TokenID(raw_val)
        return self._tok_id

    @property
    async def tok_ctrt(self) -> BaseTokCtrt:
        """
        tok_ctrt returns the token contract instance for the token used in the contract.

        Returns:
            BaseTokCtrt: The token contract instance.
        """
        if not self._tok_ctrt:
            tok_id = await self.tok_id
            self._tok_ctrt = await tcf.from_tok_id(tok_id, self.chain)
        return self._tok_ctrt

    @property
    async def unit(self) -> int:
        """
        unit returns the unit of the token specified in this contract.

        Returns:
            int: The token unit.
        """
        tc = await self.tok_ctrt
        return await tc.unit

    async def get_ctrt_bal(self, addr: str) -> md.Token:
        """
        get_ctrt_bal queries & returns the balance of the token within this contract
        belonging to the user address.

        Args:
            addr (str): The account address.

        Returns:
            md.Token: The balance of the token.
        """
        raw_val = await self._query_db_key(self.DBKey.for_contract_balance(addr))
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_chan_creator(self, chan_id: str) -> md.Addr:
        """
        get_chan_creator queries & returns the channel creator.

        Args:
            chan_id (str): The channel ID.

        Returns:
            md.Addr: The channel creator.
        """
        raw_val = await self._query_db_key(self.DBKey.for_channel_creator(chan_id))
        return md.Addr(raw_val)

    async def get_chan_creator_pub_key(self, chan_id: str) -> md.PubKey:
        """
        get_chan_creator_pub_key queries & returns the public key of the channel creator.

        Args:
            chan_id (str): The channel ID.

        Returns:
            md.PubKey: The public key of the channel creator.
        """
        raw_val = await self._query_db_key(
            self.DBKey.for_channel_creator_public_key(chan_id)
        )
        return md.PubKey(raw_val)

    async def get_chan_recipient(self, chan_id: str) -> md.Addr:
        """
        get_chan_recipient queries & returns the recipient of the channel.

        Args:
            chan_id (str): The channel ID.

        Returns:
            md.Addr: The channel recipient.
        """
        raw_val = await self._query_db_key(self.DBKey.for_channel_recipient(chan_id))
        return md.Addr(raw_val)

    async def get_chan_accum_load(self, chan_id: str) -> md.Token:
        """
        get_chan_accum_load queries & returns the accumulated load of the channel.

        Args:
            chan_id (str): The channel ID.

        Returns:
            md.Token: The accumulated load of the channel.
        """
        raw_val = await self._query_db_key(
            self.DBKey.for_channel_accumulated_load(chan_id)
        )
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_chan_accum_pay(self, chan_id: str) -> md.Token:
        """
        get_chan_accum_pay queries & returns the accumulated payment of the channel.

        Args:
            chan_id (str): The channel ID.

        Returns:
            md.Token: The accumulated payment of the channel.
        """
        raw_val = await self._query_db_key(
            self.DBKey.for_channel_accumulated_payment(chan_id)
        )
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_chan_exp_time(self, chan_id: str) -> md.VSYSTimestamp:
        """
        get_chan_exp_time queries & returns the expiration time of the channel.

        Args:
            chan_id (str): The channel ID.

        Returns:
            md.VSYSTimestamp: The expiration time of the channel.
        """
        raw_ts = await self._query_db_key(
            self.DBKey.for_channel_expiration_time(chan_id)
        )
        return md.VSYSTimestamp(raw_ts)

    async def get_chan_status(self, chan_id: str) -> bool:
        """
        get_chan_status queries & returns the status of the channel (if the channel
        is still active)

        Args:
            chan_id (str): The channel ID.

        Returns:
            bool: The status of the channel.
        """
        raw_val = await self._query_db_key(self.DBKey.for_channel_status(chan_id))
        return raw_val == "true"

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        tok_id: str,
        ctrt_description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> PayChanCtrt:
        """
        register registers a Payment Channel Contract

        Args:
            by (acnt.Account): The action taker.
            tok_id (str): The token ID.
            ctrt_description (str, optional): The description of the contract. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.RegCtrtFee.DEFAULT.

        Returns:
            PayChanCtrt: The PayChanCtrt object of the registered Payment Channel contract.
        """
        data = await by._register_contract(
            tx.RegCtrtTxReq(
                data_stack=de.DataStack(
                    de.TokenID(md.TokenID(tok_id)),
                ),
                ctrt_meta=cls.CTRT_META,
                timestamp=md.VSYSTimestamp.now(),
                description=md.Str(ctrt_description),
                fee=md.RegCtrtFee(fee),
            )
        )
        logger.debug(data)

        return cls(
            data["contractId"],
            chain=by.chain,
        )

    async def create_and_load(
        self,
        by: acnt.Account,
        recipient: str,
        amount: Union[int, float],
        expire_at: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        create_and_load creates the payment channel and loads an amount into it.
        (This function's transaction id becomes the channel ID)

        Args:
            by (acnt.Account): The action taker.
            recipient (str): The recipient account.
            amount (Union[int, float]): The amount of tokens.
            expire_at (int): Unix timestamp. When the lock will expire.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        rcpt_md = md.Addr(recipient)
        rcpt_md.must_on(self.chain)

        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.CREATE_AND_LOAD,
                data_stack=de.DataStack(
                    de.Addr(md.Addr(recipient)),
                    de.Amount.for_tok_amount(
                        amount,
                        unit,
                    ),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(expire_at)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def extend_exp_time(
        self,
        by: acnt.Account,
        chan_id: str,
        expire_at: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        extend_exp_time extends the expiration time of the channel to the new input timestamp

        Args:
            by (acnt.Account): The action taker.
            chan_id (str): The channel ID.
            expire_at (int): Unix timestamp. When the lock will expire.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.EXTEND_EXPIRATION_TIME,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(chan_id),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(expire_at)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def load(
        self,
        by: acnt.Account,
        chan_id: str,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        load loads more tokens into the channel.

        Args:
            by (acnt.Account): The action taker.
            chan_id (str): The channel ID.
            amount (Union[int, float]): The amount of tokens.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.LOAD,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(chan_id),
                    de.Amount.for_tok_amount(
                        amount,
                        unit,
                    ),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def abort(
        self,
        by: acnt.Account,
        chan_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        abort aborts the channel, triggering a 2-day grace period where the recipient can still
        collect payments. After 2 days, the payer can unload all the remaining funds that was locked
        in the channel.

        Args:
            by (acnt.Account): The action taker.
            chan_id (str): The channel ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.ABORT,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(chan_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def unload(
        self,
        by: acnt.Account,
        chan_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        unload unloads all the funcs locked in the channel (only works if the channel has expired)

        Args:
            by (acnt.Account): The action taker.
            chan_id (str): The channel ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.UNLOAD,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(chan_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def collect_payment(
        self,
        by: acnt.Account,
        chan_id: str,
        amount: Union[int, float],
        signature: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        collect_payment collects the payment from the channel.

        Args:
            by (acnt.Account): The action taker.
            chan_id (str): The channel ID.
            amount (Union[int, float]): The amount of tokens.
            signature (str): The signature in base 58 format.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        is_valid_sig = await self.verify_sig(chan_id, amount, signature)
        if not is_valid_sig:
            raise ValueError("Invalid Payment Channel Contract payment signature")

        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.COLLECT_PAYMENT,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(chan_id),
                    de.Amount.for_tok_amount(
                        amount,
                        unit,
                    ),
                    de.Bytes.from_base58_str(signature),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def offchain_pay(
        self,
        key_pair: md.KeyPair,
        chan_id: str,
        amount: Union[int, float],
    ) -> str:
        """
        offchain_pay generates the offchain payment signature.

        Args:
            key_pair (md.KeyPair): The key pair to sign.
            chan_id (str): The channel ID.
            amount (Union[int, float]): The amount of tokens.

        Returns:
            str: The signature in base58 string format.
        """
        msg = await self._get_pay_msg(chan_id, amount)
        sig_bytes = curve.sign(key_pair.pri.bytes, msg)
        return base58.b58encode(sig_bytes).decode("latin-1")

    async def verify_sig(
        self,
        chan_id: str,
        amount: Union[int, float],
        signature: str,
    ) -> bool:
        """
        verify_sig verifies the payment signature.

        Args:
            chan_id (str): The channel ID.
            amount (Union[int, float]): The amount of tokens.
            signature (str): The payment signature in base58 string format.

        Returns:
            bool: If the signature is valid.
        """
        msg = await self._get_pay_msg(chan_id, amount)
        pub_key = await self.get_chan_creator_pub_key(chan_id)
        sig_bytes = base58.b58decode(signature)
        return curve.verify_sig(pub_key.bytes, msg, sig_bytes)

    async def _get_pay_msg(
        self,
        chan_id: str,
        amount: Union[int, float],
    ) -> bytes:
        """
        _get_pay_msg generates the payment message in bytes.

        Args:
            chan_id (str): The channel ID.
            amount (Union[int, float]): The amount of tokens.

        Returns:
            bytes: The payment message.
        """
        unit = await self.unit
        raw_amount = md.Token.for_amount(amount, unit).data

        chan_id_bytes = base58.b58decode(chan_id)
        msg = (
            struct.pack(">H", len(chan_id_bytes))
            + chan_id_bytes
            + struct.pack(">Q", raw_amount)
        )
        return msg
