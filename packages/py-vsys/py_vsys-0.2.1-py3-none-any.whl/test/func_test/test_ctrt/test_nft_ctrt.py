import abc

import pytest

import py_vsys as pv
from test.func_test import conftest as cft


class TestNFTCtrt:
    """
    TestNFTCtrt is the collection of functional tests of NFT contract.
    """

    @pytest.fixture
    async def new_ctrt(self, acnt0: pv.Account) -> pv.NFTCtrt:
        """
        new_ctrt is the fixture that registers a new NFT contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.NFTCtrt: The NFTCtrt instance.
        """
        nc = await pv.NFTCtrt.register(acnt0)
        await cft.wait_for_block()
        return nc

    @pytest.fixture
    async def new_ctrt_with_tok(
        self, new_ctrt: pv.NFTCtrt, acnt0: pv.Account
    ) -> pv.NFTCtrt:
        """
        new_ctrt_with_tok is the fixture that registers a new NFT contract and issues an NFT token right after it.

        Args:
            new_ctrt (pv.NFTCtrt): The fixture that registers a new NFT contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.NFTCtrt: The NFTCtrt instance.
        """
        nc = new_ctrt
        await nc.issue(acnt0)
        await cft.wait_for_block()
        return nc

    @pytest.fixture
    async def new_atomic_swap_ctrt(
        self,
        new_ctrt_with_tok: pv.NFTCtrt,
        acnt0: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        nc = new_ctrt_with_tok

        tok_id = pv.Ctrt.get_tok_id(nc.ctrt_id, pv.TokenIdx(0))
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id.data)

        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr
        assert (await ac.tok_id) == tok_id

        return ac

    async def test_register(self, acnt0: pv.Account) -> pv.NFTCtrt:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.NFTCtrt: The registered NFTCtrt.
        """
        nc = await pv.NFTCtrt.register(acnt0)
        await cft.wait_for_block()
        assert (await nc.issuer) == acnt0.addr
        assert (await nc.maker) == acnt0.addr

        return nc

    async def test_issue(self, new_ctrt: pv.NFTCtrt, acnt0: pv.Account):
        """
        test_issue tests the method issue.

        Args:
            new_ctrt (pv.NFTCtrt): The fixture that registers a new NFT contract.
            acnt0 (pv.Account): The account of nonce 0.
        """
        nc = new_ctrt
        api = nc.chain.api

        resp = await nc.issue(acnt0)
        await cft.wait_for_block()

        await cft.assert_tx_success(api, resp["id"])

        tok_id = pv.Ctrt.get_tok_id(nc.ctrt_id, pv.TokenIdx(0))
        tok_bal = await cft.get_tok_bal(api, acnt0.addr.data, tok_id.data)
        assert tok_bal == 1

    async def test_send(
        self, new_ctrt_with_tok: pv.NFTCtrt, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_send tests the method send

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = pv.Ctrt.get_tok_id(nc.ctrt_id, pv.TokenIdx(0))

        tok_bal_acnt0 = await cft.get_tok_bal(api, acnt0.addr.data, tok_id.data)
        assert tok_bal_acnt0 == 1

        tok_bal_acnt1 = await cft.get_tok_bal(api, acnt1.addr.data, tok_id.data)
        assert tok_bal_acnt1 == 0

        resp = await nc.send(acnt0, acnt1.addr.data, 0)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_bal_acnt0 = await cft.get_tok_bal(api, acnt0.addr.data, tok_id.data)
        assert tok_bal_acnt0 == 0

        tok_bal_acnt1 = await cft.get_tok_bal(api, acnt1.addr.data, tok_id.data)
        assert tok_bal_acnt1 == 1

    async def test_transfer(
        self, new_ctrt_with_tok: pv.NFTCtrt, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_transfer tests the method transfer.

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = pv.Ctrt.get_tok_id(nc.ctrt_id, pv.TokenIdx(0))

        tok_bal_acnt0 = await cft.get_tok_bal(api, acnt0.addr.data, tok_id.data)
        assert tok_bal_acnt0 == 1

        tok_bal_acnt1 = await cft.get_tok_bal(api, acnt1.addr.data, tok_id.data)
        assert tok_bal_acnt1 == 0

        resp = await nc.transfer(acnt0, acnt0.addr.data, acnt1.addr.data, 0)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_bal_acnt0 = await cft.get_tok_bal(api, acnt0.addr.data, tok_id.data)
        assert tok_bal_acnt0 == 0

        tok_bal_acnt1 = await cft.get_tok_bal(api, acnt1.addr.data, tok_id.data)
        assert tok_bal_acnt1 == 1

    async def test_deposit_withdraw(
        self,
        new_ctrt_with_tok: pv.NFTCtrt,
        new_atomic_swap_ctrt: pv.AtomicSwapCtrt,
        acnt0: pv.Account,
    ):
        """
        test_deposit_withdraw tests the method deposit & withdraw.

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            new_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract.
            acnt0 (pv.Account): The account of nonce 0.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = pv.Ctrt.get_tok_id(nc.ctrt_id, pv.TokenIdx(0))
        ac = new_atomic_swap_ctrt

        tok_bal = await cft.get_tok_bal(api, acnt0.addr.data, tok_id.data)
        assert tok_bal == 1

        resp = await nc.deposit(acnt0, ac.ctrt_id.data, 0)
        await cft.wait_for_block()
        tx_info = await api.tx.get_info(resp["id"])
        assert tx_info["status"] == "Success"

        tok_bal = await cft.get_tok_bal(api, acnt0.addr.data, tok_id.data)
        assert tok_bal == 0

        deposited_tok_bal = await ac.get_ctrt_bal(acnt0.addr.data)
        assert deposited_tok_bal.amount == 1

        await nc.withdraw(acnt0, ac.ctrt_id.data, 0)
        await cft.wait_for_block()

        tok_bal = await cft.get_tok_bal(api, acnt0.addr.data, tok_id.data)
        assert tok_bal == 1

        deposited_tok_bal = await ac.get_ctrt_bal(acnt0.addr.data)
        assert deposited_tok_bal.amount == 0

    async def test_supersede(
        self, new_ctrt: pv.NFTCtrt, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_supersede tests the method supersede.

        Args:
            new_ctrt (pv.NFTCtrt): The fixture that registers a new NFT contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        nc = new_ctrt
        api = nc.chain.api

        assert (await nc.issuer) == acnt0.addr

        resp = await nc.supersede(acnt0, acnt1.addr.data)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await nc.issuer) == acnt1.addr

    @pytest.mark.whole
    async def test_as_whole(
        self,
        new_ctrt_with_tok: pv.NFTCtrt,
        new_atomic_swap_ctrt: pv.AtomicSwapCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):

        """
        test_as_whole tests methods of NFTCtrt as a whole so as to reduce resource consumption.

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            new_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        nc = await self.test_register(acnt0)
        await self.test_issue(nc, acnt0)

        nc = new_ctrt_with_tok
        ac = new_atomic_swap_ctrt

        await self.test_send(nc, acnt0, acnt1)
        await self.test_transfer(nc, acnt1, acnt0)
        await self.test_deposit_withdraw(nc, ac, acnt0)
        await self.test_supersede(nc, acnt0, acnt1)


class _TestNFTCtrtV2Base(TestNFTCtrt):
    """
    _TestNFTCtrtV2Base is the collection of general functional tests of NFT contract V2.
    """

    @pytest.fixture
    @abc.abstractmethod
    async def new_ctrt(self, acnt0: pv.Account, acnt1: pv.Account) -> pv.NFTCtrtV2Base:
        """
        new_ctrt is the fixture that registers a new NFT contract V2 instance.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.

        Returns:
            pv.NFTCtrtV2Base: The pv.NFTCtrtV2Base instance.
        """

    @pytest.fixture
    @abc.abstractmethod
    async def new_atomic_swap_ctrt(
        self,
        new_ctrt_with_tok: pv.NFTCtrtV2Blacklist,
        acnt0: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_ctrt_with_tok (pv.NFTCtrtV2Base): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """

    @pytest.fixture
    def arbitrary_ctrt_id(self) -> str:
        """
        arbitrary_ctrt_id is the fixture that returns an arbitrary contract ID

        Returns:
            str: The contract ID.
        """
        return "CF5Zkj2Ycx72WrBnjrcNHvJRVwsbNX1tjgT"

    async def test_supersede(
        self, new_ctrt: pv.NFTCtrtV2Whitelist, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_supersede tests the method supersede.

        Args:
            new_ctrt (pv.NFTCtrtV2Whitelist): The fixture that registers a new NFT contract V2 with whitelist.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """

        nc = new_ctrt
        api = nc.chain.api

        assert (await nc.issuer) == acnt0.addr
        assert (await nc.regulator) == acnt0.addr

        resp = await nc.supersede(acnt0, acnt1.addr.data, acnt1.addr.data)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await nc.issuer) == acnt1.addr
        assert (await nc.regulator) == acnt1.addr

    async def test_update_list_user(
        self, new_ctrt: pv.NFTCtrtV2Whitelist, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_update_list_user tests the method update_list_user.

        Args:
            new_ctrt (pv.NFTCtrtV2Whitelist): The fixture that registers a new NFT contract V2 with whitelist.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """

        nc = new_ctrt
        api = nc.chain.api

        in_list = await nc.is_user_in_list(acnt1.addr.data)
        assert in_list == False

        resp = await nc.update_list_user(
            by=acnt0,
            addr=acnt1.addr.data,
            val=True,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await nc.is_user_in_list(acnt1.addr.data)
        assert in_list == True

        resp = await nc.update_list_user(
            by=acnt0,
            addr=acnt1.addr.data,
            val=False,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await nc.is_user_in_list(acnt1.addr.data)
        assert in_list == False

    async def test_update_list_ctrt(
        self, new_ctrt: pv.NFTCtrtV2Whitelist, acnt0: pv.Account, arbitrary_ctrt_id: str
    ):
        """
        test_update_list_ctrt tests the method update_list_ctrt.

        Args:
            new_ctrt (pv.NFTCtrtV2Whitelist): The fixture that registers a new NFT contract V2 with whitelist.
            acnt0 (pv.Account): The account of nonce 0.
            arbitrary_ctrt_id (str): An arbitrary contract ID
        """
        nc = new_ctrt
        api = nc.chain.api
        target_ctrt_id = arbitrary_ctrt_id

        in_list = await nc.is_ctrt_in_list(target_ctrt_id)
        assert in_list == False

        resp = await nc.update_list_ctrt(
            by=acnt0,
            addr=target_ctrt_id,
            val=True,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await nc.is_ctrt_in_list(target_ctrt_id)
        assert in_list == True

        resp = await nc.update_list_ctrt(
            by=acnt0,
            addr=target_ctrt_id,
            val=False,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await nc.is_ctrt_in_list(target_ctrt_id)
        assert in_list == False

    async def test_register(self, acnt0: pv.Account) -> pv.NFTCtrtV2Whitelist:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.NFTCtrtV2Whitelist: The registered NFTCtrtV2Whitelist
        """
        nc: pv.NFTCtrtV2Whitelist = await pv.NFTCtrtV2Whitelist.register(acnt0)
        await cft.wait_for_block()
        assert (await nc.issuer) == acnt0.addr
        assert (await nc.maker) == acnt0.addr
        assert (await nc.regulator) == acnt0.addr

        return nc

    @pytest.mark.whole
    async def test_as_whole(
        self,
        new_ctrt_with_tok: pv.NFTCtrtV2Whitelist,
        new_atomic_swap_ctrt: pv.AtomicSwapCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
        arbitrary_ctrt_id: str,
    ):
        """
        test_as_whole tests method of NFTCtrtV2Whitelist as a whole so as to reduce resource consumption.

        Args:
            new_ctrt_with_tok (pv.NFTCtrtV2Whitelist): The fixture that registers a new NFT contract and issues an NFT token right after it.
            new_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            arbitrary_ctrt_id (str): An arbitrary contract ID
        """
        nc = await self.test_register(acnt0)
        await self.test_update_list_user(nc, acnt0, acnt1)
        await self.test_update_list_ctrt(nc, acnt0, arbitrary_ctrt_id)

        await self.test_issue(nc, acnt0)

        nc = new_ctrt_with_tok
        ac = new_atomic_swap_ctrt

        await self.test_send(nc, acnt0, acnt1)
        await self.test_transfer(nc, acnt1, acnt0)

        await self.test_deposit_withdraw(nc, ac, acnt0)
        await self.test_supersede(nc, acnt0, acnt1)


class TestNFTCtrtV2Whitelist(_TestNFTCtrtV2Base):
    """
    TestNFTCtrtV2Whitelist is the collection of functional tests of NFT contract V2 with whitelist.
    """

    @pytest.fixture
    async def new_ctrt(
        self, acnt0: pv.Account, acnt1: pv.Account
    ) -> pv.NFTCtrtV2Whitelist:
        """
        new_ctrt is the fixture that registers a new NFT contract V2 with whitelist.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.

        Returns:
            pv.NFTCtrtV2Whitelist: The NFTCtrtV2Whitelist instance.
        """
        nc = await pv.NFTCtrtV2Whitelist.register(acnt0)
        await cft.wait_for_block()

        await nc.update_list_user(acnt0, acnt0.addr.data, True)
        await nc.update_list_user(acnt0, acnt1.addr.data, True)
        return nc

    @pytest.fixture
    async def new_atomic_swap_ctrt(
        self,
        new_ctrt_with_tok: pv.NFTCtrtV2Whitelist,
        acnt0: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_ctrt_with_tok (pv.NFTCtrtV2Whitelist): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = pv.Ctrt.get_tok_id(nc.ctrt_id, pv.TokenIdx(0))
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id.data)

        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr
        assert (await ac.tok_id) == tok_id

        resp = await nc.update_list_ctrt(acnt0, ac.ctrt_id.data, True)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        return ac


class TestNFTCtrtV2Blacklist(_TestNFTCtrtV2Base):
    """
    TestNFTCtrtV2Blacklist is the collection of functional tests of NFT contract V2 with blacklist.
    """

    @pytest.fixture
    async def new_ctrt(self, acnt0: pv.Account) -> pv.NFTCtrtV2Blacklist:
        """
        new_ctrt is the fixture that registers a new NFT contract V2 with blacklist.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.

        Returns:
            pv.NFTCtrtV2Blacklist: The NFTCtrtV2Blacklist instance.
        """
        nc = await pv.NFTCtrtV2Blacklist.register(acnt0)
        await cft.wait_for_block()

        return nc

    @pytest.fixture
    async def new_atomic_swap_ctrt(
        self,
        new_ctrt_with_tok: pv.NFTCtrtV2Blacklist,
        acnt0: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_ctrt_with_tok (pv.NFTCtrtV2Blacklist): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        nc = new_ctrt_with_tok

        tok_id = pv.Ctrt.get_tok_id(nc.ctrt_id, pv.TokenIdx(0))
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id.data)

        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr
        assert (await ac.tok_id) == tok_id

        return ac
