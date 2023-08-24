TORTOISE_ORM = {
    "connections": {"default": "mysql://root:123123@42.193.248.250:13306/test_db"},
    "apps": {
        "myfastapi": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}