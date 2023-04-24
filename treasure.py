TREASURE_NOT_EXIST_TEMPLATE = """<html><head><title>Treasure not exist</title></head><body><p>treasure {id} not exist</p></body></html>"""
TREASURE_NOT_COLLECTED_TEMPLATE = """<html><head><title>Treasure not collected</title></head><body><p>treasure {id} not collected</p></body></html>"""
TREASURE_USE_SUCCESS_TEMPLATE = """<html><head><title>Treasure used success</title></head><body><p>Success to use the treasure {id}, type:{treasureType}</p></body></html>"""
TREASUE_USE_FAIL_TEMPLATE = """<html><head><title>unavailable to use the treasure</title></head><body>    <p>Fail to use treasure {id}, type:{treasureType}</p><p>{reason}</p></body></html>"""
TREASURE_ALREADY_USED_TEMPLATE = """<html>
    <head>
        <title>
        Treasure already used
        </title>
    </head>
    <body>
    <p>You can not use this treasure, because it has already been used.</p>
    </body>
</html>"""
TREASURE_COLLECT_SUCCESS_TEMPLATE = """<html><head><title>Treasure collect success</title></head><body><p>You collected a {treasureType}, you can use it in <a href="/treasures/">you treasures</a>/p></body></html>"""
TREASURE_UNABLE_COLLECT_TEMPLATE = """<html><head><title>ALREADY COLLECTED</title></head><body><p>This treasue (id={id}) has already be collected or used, so you can't collect this one./p></body></html>"""
MY_TREASURES_TEMPLATE_HEAD = """<html>
    <head>
        <title>
        My Treasures
        </title>
    </head>
    <body>
        <h1>My treasures</h1>
        <ul>
    """
MY_TREASURE_ITEM_TEMPLATE = """<li><span>{treasureType}</span><a href="/treasure/use/{id}">use</a></li>"""
MY_TREASURES_TEMPLATE_TAIL = """
    </ul>
    </body>
</html>
"""