from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `users` RENAME COLUMN `test_column6` TO `test_column9`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `users` RENAME COLUMN `test_column9` TO `test_column6`;"""
