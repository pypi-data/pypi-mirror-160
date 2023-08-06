"""
v_swap_ctrt contains V Swap contract.
"""
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any, Dict, Union, Optional

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_vsys import account as acnt
    from py_vsys import chain as ch

from py_vsys import data_entry as de
from py_vsys import tx_req as tx
from py_vsys import model as md
from py_vsys.contract import tok_ctrt_factory as tcf
from . import Ctrt, BaseTokCtrt


class VSwapCtrt(Ctrt):
    """
    VSwapCtrt is the class for VSYS V Swap contract.

    NOTE that when it comes to the tokens in the pool, the terms "base/target" & "A/B" can be used interchangeably.
    i.e. base token <=> token A
         target token <=> token B
    """

    CTRT_META = md.CtrtMeta.from_b58_str(
        "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"
    )

    class FuncIdx(Ctrt.FuncIdx):
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        SUPERSEDE = 0
        SET_SWAP = 1
        ADD_LIQUIDITY = 2
        REMOVE_LIQUIDITY = 3
        SWAP_B_FOR_EXACT_A = 4
        SWAP_EXACT_B_FOR_A = 5
        SWAP_A_FOR_EXACT_B = 6
        SWAP_EXACT_A_FOR_B = 7

    class StateVar(Ctrt.StateVar):
        """
        StateVar is the enum class for state variables of a contract.
        """

        MAKER = 0
        TOKEN_A_ID = 1
        TOKEN_B_ID = 2
        LIQUIDITY_TOKEN_ID = 3
        SWAP_STATUS = 4
        MINIMUM_LIQUIDITY = 5
        TOKEN_A_RESERVED = 6
        TOKEN_B_RESERVED = 7
        TOTAL_SUPPLY = 8
        LIQUIDITY_TOKEN_LEFT = 9

    class StateMapIdx(Ctrt.StateMapIdx):
        """
        StateMapIdx is the enum class for state map indexes.
        """

        TOKEN_A_BALANCE = 0
        TOKEN_B_BALANCE = 1
        LIQUIDITY_TOKEN_BALANCE = 2

    class DBKey(Ctrt.DBKey):
        """
        DBKey is the class for DB key of a contract used to query data.
        """

        @classmethod
        def for_maker(cls) -> VSwapCtrt.DBKey:
            """
            for_maker returns the VSwapCtrt.DBKey object for querying
            the address of the maker of the contract.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateVar.MAKER.serialize()
            return cls(b)

        @classmethod
        def for_tok_a_id(cls) -> VSwapCtrt.DBKey:
            """
            for_tok_a_id returns the VSwapCtrt.DBKey object for querying
            the token A ID.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateVar.TOKEN_A_ID.serialize()
            return cls(b)

        @classmethod
        def for_tok_b_id(cls) -> VSwapCtrt.DBKey:
            """
            for_tok_b_id returns the VSwapCtrt.DBKey object for querying
            the token B ID.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateVar.TOKEN_B_ID.serialize()
            return cls(b)

        @classmethod
        def for_liq_tok_id(cls) -> VSwapCtrt.DBKey:
            """
            for_liq_tok_id returns the VSwapCtrt.DBKey object for querying
            the liquidity token ID.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateVar.LIQUIDITY_TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_swap_status(cls) -> VSwapCtrt.DBKey:
            """
            for_swap_status returns the VSwapCtrt.DBKey object for querying
            the swap status of whether or not the swap is currently active.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateVar.SWAP_STATUS.serialize()
            return cls(b)

        @classmethod
        def for_min_liq(cls) -> VSwapCtrt.DBKey:
            """
            for_min_liq returns the VSwapCtrt.DBKey object for querying
            the minimum liquidity for the pool. This liquidity cannot be withdrawn.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateVar.MINIMUM_LIQUIDITY.serialize()
            return cls(b)

        @classmethod
        def for_tok_a_reserved(cls) -> VSwapCtrt.DBKey:
            """
            for_tok_a_reserved returns the VSwapCtrt.DBKey object for querying
            the amount of token A inside the pool.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateVar.TOKEN_A_RESERVED.serialize()
            return cls(b)

        @classmethod
        def for_tok_b_reserved(cls) -> VSwapCtrt.DBKey:
            """
            for_tok_b_reserved returns the VSwapCtrt.DBKey object for querying
            the amount of token B inside the pool.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateVar.TOKEN_B_RESERVED.serialize()
            return cls(b)

        @classmethod
        def for_total_liq_tok_supply(cls) -> VSwapCtrt.DBKey:
            """
            for_total_liq_tok_supply returns the VSwapCtrt.DBKey object for querying
            the total amount of liquidity tokens that can be minted.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateVar.TOTAL_SUPPLY.serialize()
            return cls(b)

        @classmethod
        def for_liq_tok_left(cls) -> VSwapCtrt.DBKey:
            """
            for_liq_tok_left returns the VSwapCtrt.DBKey object for querying
            the amount of liquidity tokens left to be minted.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateVar.LIQUIDITY_TOKEN_LEFT.serialize()
            return cls(b)

        @classmethod
        def for_tok_a_bal(cls, addr: str) -> VSwapCtrt.DBKey:
            """
            for_tok_a_bal returns the VSwapCtrt.DBKey object for querying
            the balance of token A stored within the contract belonging to the
            given user address.

            Args:
                addr (str): The address of the user.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateMap(
                idx=VSwapCtrt.StateMapIdx.TOKEN_A_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_tok_b_bal(cls, addr: str) -> VSwapCtrt.DBKey:
            """
            for_tok_b_bal returns the VSwapCtrt.DBKey object for querying
            the balance of token B stored within the contract belonging to the
            given user address.

            Args:
                addr (str): The address of the user.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateMap(
                idx=VSwapCtrt.StateMapIdx.TOKEN_B_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_liq_tok_bal(cls, addr: str) -> VSwapCtrt.DBKey:
            """
            for_liq_tok_bal returns the VSwapCtrt.DBKey object for querying
            the balance of liquidity token stored within the contract belonging to the
            given user address.

            Args:
                addr (str): The address of the user.

            Returns:
                VSwapCtrt.DBKey: The VSwapCtrt.DBKey object.
            """
            b = VSwapCtrt.StateMap(
                idx=VSwapCtrt.StateMapIdx.LIQUIDITY_TOKEN_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

    def __init__(
        self,
        ctrt_id: str,
        chain: ch.Chain,
    ) -> None:
        """
        Args:
            ctrt_id (str): The id of the contract.
            chain (ch.Chain): The object of the chain where the contract is on.
        """
        self._ctrt_id = md.CtrtID(ctrt_id)
        self._chain = chain

        self._tok_a_id: Optional[md.TokenID] = None
        self._tok_b_id: Optional[md.TokenID] = None
        self._liq_tok_id: Optional[md.TokenID] = None
        self._tok_a_ctrt: Optional[BaseTokCtrt] = None
        self._tok_b_ctrt: Optional[BaseTokCtrt] = None
        self._liq_tok_ctrt: Optional[BaseTokCtrt] = None

        self._min_liq: Optional[md.Token] = None

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
    async def tok_a_id(self) -> md.TokenID:
        """
        tok_a_id queries & returns the token A ID of the contract.

        Returns:
            md.TokenID: The token A ID of the contract.
        """
        if not self._tok_a_id:
            raw_val = await self._query_db_key(self.DBKey.for_tok_a_id())
            self._tok_a_id = md.TokenID(raw_val)
        return self._tok_a_id

    @property
    async def tok_b_id(self) -> md.TokenID:
        """
        tok_b_id queries & returns the token B ID of the contract.

        Returns:
            md.TokenID: The token B ID of the contract.
        """
        if not self._tok_b_id:
            raw_val = await self._query_db_key(self.DBKey.for_tok_b_id())
            self._tok_b_id = md.TokenID(raw_val)
        return self._tok_b_id

    @property
    async def liq_tok_id(self) -> md.TokenID:
        """
        liq_tok_id queries & returns the liquidity token ID of the contract.

        Returns:
            md.TokenID: The liquidity token ID of the contract.
        """
        if not self._liq_tok_id:
            raw_val = await self._query_db_key(self.DBKey.for_liq_tok_id())
            self._liq_tok_id = md.TokenID(raw_val)
        return self._liq_tok_id

    @property
    async def tok_a_ctrt(self) -> BaseTokCtrt:
        """
        tok_a_ctrt returns the token contract intance for token A.

        Returns:
            BaseTokCtrt: The token contract intance.
        """
        if not self._tok_a_ctrt:
            tok_a_id = await self.tok_a_id
            self._tok_a_ctrt = await tcf.from_tok_id(tok_a_id, self.chain)
        return self._tok_a_ctrt

    @property
    async def tok_b_ctrt(self) -> BaseTokCtrt:
        """
        tok_b_ctrt returns the token contract intance for token B.

        Returns:
            BaseTokCtrt: The token contract intance.
        """
        if not self._tok_b_ctrt:
            tok_b_id = await self.tok_b_id
            self._tok_b_ctrt = await tcf.from_tok_id(tok_b_id, self.chain)
        return self._tok_b_ctrt

    @property
    async def liq_tok_ctrt(self) -> BaseTokCtrt:
        """
        liq_tok_ctrt returns the token contract intance for liquidity token.

        Returns:
            BaseTokCtrt: The token contract intance.
        """
        if not self._liq_tok_ctrt:
            liq_tok_id = await self.liq_tok_id
            self._liq_tok_ctrt = await tcf.from_tok_id(liq_tok_id, self.chain)
        return self._liq_tok_ctrt

    @property
    async def tok_a_unit(self) -> int:
        """
        tok_a_unit returns the unit of token A.

        Returns:
            int: The unit of token A.
        """
        tc = await self.tok_a_ctrt
        return await tc.unit

    @property
    async def tok_b_unit(self) -> int:
        """
        tok_b_unit returns the unit of token B.

        Returns:
            int: The unit of token B.
        """
        tc = await self.tok_b_ctrt
        return await tc.unit

    @property
    async def liq_tok_unit(self) -> int:
        """
        liq_tok_unit returns the unit of liquidity token.

        Returns:
            int: The unit of liquidity token.
        """
        tc = await self.liq_tok_ctrt
        return await tc.unit

    @property
    async def is_swap_active(self) -> bool:
        """
        swap_status queries & returns the swap status of whether or not
        the swap is currently active.

        Returns:
            bool: Whether or not the swap is currently active.
        """
        data = await self._query_db_key(self.DBKey.for_swap_status())
        return data == "true"

    @property
    async def min_liq(self) -> md.Token:
        """
        min_liq queries & returns the minimum liquidity of the contract.

        Returns:
            md.Token: The minimum liquidity of the contract.
        """
        if self._min_liq == 0:
            raw_val = await self._query_db_key(self.DBKey.for_min_liq())
            unit = await self.liq_tok_unit
            self._min_liq = md.Token(raw_val, unit)
        return self._min_liq

    @property
    async def tok_a_reserved(self) -> md.Token:
        """
        tok_a_reserved queries & returns the amount of token A inside the pool.

        Returns:
            md.Token: The amount of token A inside the pool.
        """
        raw_val = await self._query_db_key(self.DBKey.for_tok_a_reserved())
        unit = await self.tok_a_unit
        return md.Token(raw_val, unit)

    @property
    async def tok_b_reserved(self) -> md.Token:
        """
        tok_b_reserved queries & returns the amount of token B inside the pool.

        Returns:
            md.Token: The amount of token B inside the pool.
        """
        raw_val = await self._query_db_key(self.DBKey.for_tok_b_reserved())
        unit = await self.tok_b_unit
        return md.Token(raw_val, unit)

    @property
    async def total_liq_tok_supply(self) -> md.Token:
        """
        total_liq_tok_supply queries & returns the total amount of liquidity tokens
        that can be minted.

        Returns:
            md.Token: The total amount of liquidity tokens that can be minted.
        """
        raw_val = await self._query_db_key(self.DBKey.for_total_liq_tok_supply())
        unit = await self.liq_tok_unit
        return md.Token(raw_val, unit)

    @property
    async def liq_tok_left(self) -> md.Token:
        """
        liq_tok_left queries & returns the amount of liquidity tokens left to be minted.

        Returns:
            int: The amount of liquidity tokens left to be minted.
        """
        raw_val = await self._query_db_key(self.DBKey.for_liq_tok_left())
        unit = await self.liq_tok_unit
        return md.Token(raw_val, unit)

    async def get_tok_a_bal(self, addr: str) -> md.Token:
        """
        get_tok_a_bal queries & returns the balance of token A stored within the contract belonging
        to the given user address.

        Args:
            addr (str): The address of the user.

        Returns:
            md.Token: The balance.
        """
        raw_val = await self._query_db_key(self.DBKey.for_tok_a_bal(addr))
        unit = await self.tok_a_unit
        return md.Token(raw_val, unit)

    async def get_tok_b_bal(self, addr: str) -> md.Token:
        """
        get_tok_b_bal queries & returns the balance of token B stored within the contract belonging
        to the given user address.

        Args:
            addr (str): The address of the user.

        Returns:
            md.Token: The balance.
        """
        raw_val = await self._query_db_key(self.DBKey.for_tok_b_bal(addr))
        unit = await self.tok_b_unit
        return md.Token(raw_val, unit)

    async def get_liq_tok_bal(self, addr: str) -> md.Token:
        """
        get_liq_tok_bal queries & returns the balance of the liquidity token stored within the contract belonging
        to the given user address.

        Args:
            addr (str): The address of the user.

        Returns:
            md.Token: The balance.
        """
        raw_val = await self._query_db_key(self.DBKey.for_liq_tok_bal(addr))
        unit = await self.liq_tok_unit
        return md.Token(raw_val, unit)

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        tok_a_id: str,
        tok_b_id: str,
        liq_tok_id: str,
        min_liq: int,
        ctrt_description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> VSwapCtrt:
        """
        register registers a V Swap contract.

        Args:
            by (acnt.Account): The action taker.
            tok_a_id (str): The ID of token A.
            tok_b_id (str): The ID of token B.
            liq_tok_id (str): The ID of liquidity token.
            min_liq (int): The minimum liquidity of the contract.
            ctrt_description (str, optional): The description of the contract. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.RegCtrtFee.DEFAULT.

        Returns:
            VSwapCtrt: The VSwapCtrt object of the registered contract.
        """
        data = await by._register_contract(
            tx.RegCtrtTxReq(
                data_stack=de.DataStack(
                    de.TokenID(md.TokenID(tok_a_id)),
                    de.TokenID(md.TokenID(tok_b_id)),
                    de.TokenID(md.TokenID(liq_tok_id)),
                    de.Amount(md.NonNegativeInt(min_liq)),
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

    async def supersede(
        self,
        by: acnt.Account,
        new_owner: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        supersede transfers the contract rights of the contract to a new account.

        Args:
            by (acnt.Account): The action taker.
            new_owner (str): The account address of the new owner.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        new_owner_md = md.Addr(new_owner)
        new_owner_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SUPERSEDE,
                data_stack=de.DataStack(
                    de.Addr(new_owner_md),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def set_swap(
        self,
        by: acnt.Account,
        amount_a: Union[int, float],
        amount_b: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        set_swap creates a swap and deposit initial amounts into the pool

        Args:
            by (acnt.Account): The action taker.
            amount_a (int): The initial amount for token A.
            amount_b (int): The initial amount for token B.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        tok_a_unit, tok_b_unit = await asyncio.gather(
            self.tok_a_unit,
            self.tok_b_unit,
        )

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SET_SWAP,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount_a, tok_a_unit),
                    de.Amount.for_tok_amount(amount_b, tok_b_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def add_liquidity(
        self,
        by: acnt.Account,
        amount_a: Union[int, float],
        amount_b: Union[int, float],
        amount_a_min: Union[int, float],
        amount_b_min: Union[int, float],
        deadline: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        add_liquidity adds liquidity to the pool. The final added amount of token A & B will
        be in the same proportion as the pool at that moment as the liquidity provider shouldn't
        change the price of the token while the price is determined by the ratio between A & B.

        Args:
            by (acnt.Account): The action taker.
            amount_a (Union[int, float]): The desired amount of token A.
            amount_b (Union[int, float]): The desired amount of token B.
            amount_a_min (Union[int, float]): The minimum acceptable amount of token A.
            amount_b_min (Union[int, float]): The minimum acceptable amount of token B.
            deadline (int): Unix timestamp. The deadline for this operation to complete.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """
        tok_a_unit, tok_b_unit = await asyncio.gather(
            self.tok_a_unit,
            self.tok_b_unit,
        )

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.ADD_LIQUIDITY,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount_a, tok_a_unit),
                    de.Amount.for_tok_amount(amount_b, tok_b_unit),
                    de.Amount.for_tok_amount(amount_a_min, tok_a_unit),
                    de.Amount.for_tok_amount(amount_b_min, tok_b_unit),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(deadline)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def remove_liquidity(
        self,
        by: acnt.Account,
        amount_liq: Union[int, float],
        amount_a_min: Union[int, float],
        amount_b_min: Union[int, float],
        deadline: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        remove_liquidity removes liquidity from the pool by redeeming token A & B with liquidity tokens.

        Args:
            by (acnt.Account): The action taker.
            amount_liq (Union[int, float]): The amount of liquidity token to return.
            amount_a_min (Union[int, float]): The minimum acceptable amount of token A to redeem.
            amount_b_min (Union[int, float]): The minimum acceptable amount of token B to redeem.
            deadline (int): Unix timestamp. The deadline for this operation to complete.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        tok_a_unit, tok_b_unit, liq_tok_unit = await asyncio.gather(
            self.tok_a_unit,
            self.tok_b_unit,
            self.liq_tok_unit,
        )

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.REMOVE_LIQUIDITY,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount_liq, liq_tok_unit),
                    de.Amount.for_tok_amount(amount_a_min, tok_a_unit),
                    de.Amount.for_tok_amount(amount_b_min, tok_b_unit),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(deadline)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def swap_b_for_exact_a(
        self,
        by: acnt.Account,
        amount_a: Union[int, float],
        amount_b_max: Union[int, float],
        deadline: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        swap_b_for_exact_a swaps token B for token A where the desired amount of token A is fixed.

        Args:
            by (acnt.Account): The action taker.
            amount_a (Union[int, float]): The desired amount of token A.
            amount_b_max (Union[int, float]): The maximum amount of token B the action taker is willing to pay.
            deadline (int): Unix timestamp. The deadline for this operation to complete.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        tok_a_unit, tok_b_unit = await asyncio.gather(
            self.tok_a_unit,
            self.tok_b_unit,
        )

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SWAP_B_FOR_EXACT_A,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount_a, tok_a_unit),
                    de.Amount.for_tok_amount(amount_b_max, tok_b_unit),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(deadline)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def swap_exact_b_for_a(
        self,
        by: acnt.Account,
        amount_a_min: Union[int, float],
        amount_b: Union[int, float],
        deadline: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        swap_exact_b_for_a swaps token B for token A where the amount of token B to pay is fixed.

        Args:
            by (acnt.Account): The action taker.
            amount_a_min (Union[int, float]): The minimum acceptable amount of token A.
            amount_b (Union[int, float]): The amount of token B to pay.
            deadline (int): Unix timestamp. The deadline for this operation to complete.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        tok_a_unit, tok_b_unit = await asyncio.gather(
            self.tok_a_unit,
            self.tok_b_unit,
        )

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SWAP_EXACT_B_FOR_A,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount_a_min, tok_a_unit),
                    de.Amount.for_tok_amount(amount_b, tok_b_unit),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(deadline)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def swap_a_for_exact_b(
        self,
        by: acnt.Account,
        amount_b: Union[int, float],
        amount_a_max: Union[int, float],
        deadline: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        swap_a_for_exact_b swaps token A for token B where the desired amount of token B is fixed.

        Args:
            by (acnt.Account): The action taker.
            amount_b (Union[int, float]): The desired amount of token B.
            amount_a_max (Union[int, float]): The maximum amount of token A the action taker is willing to pay.
            deadline (int): Unix timestamp. The deadline for this operation to complete.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        tok_a_unit, tok_b_unit = await asyncio.gather(
            self.tok_a_unit,
            self.tok_b_unit,
        )

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SWAP_A_FOR_EXACT_B,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount_b, tok_b_unit),
                    de.Amount.for_tok_amount(amount_a_max, tok_a_unit),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(deadline)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def swap_exact_a_for_b(
        self,
        by: acnt.Account,
        amount_b_min: Union[int, float],
        amount_a: Union[int, float],
        deadline: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        swap_exact_a_for_b swaps token A for token B where the amount of token A to pay is fixed.

        Args:
            by (acnt.Account): The action taker.
            amount_b_min (Union[int, float]): The minimum acceptable amount of token B.
            amount_a (Union[int, float]): The amount of token A to pay.
            deadline (int): Unix timestamp. The deadline for this operation to complete.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        tok_a_unit, tok_b_unit = await asyncio.gather(
            self.tok_a_unit,
            self.tok_b_unit,
        )

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SWAP_EXACT_A_FOR_B,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount_b_min, tok_b_unit),
                    de.Amount.for_tok_amount(amount_a, tok_a_unit),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(deadline)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data
