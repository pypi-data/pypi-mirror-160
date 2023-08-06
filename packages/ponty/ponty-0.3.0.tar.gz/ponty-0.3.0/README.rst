Ponty: Minimal async server framework
=====================================


Ponty is a simple wrapper on `aiohttp <https://github.com/aio-libs/aiohttp>`_.



Hello World
-----------

.. code-block:: python

    from ponty import (
        startmeup, get, render, expect,
        Request, StringRouteParameter,
    )


    class Req(Request):

      name = StringRouteParameter()


    @get(f"/hello/{Req.name}")
    @expect(Req)
    @render
    async def hw(name: str):
        return {"greeting": f"hi {name}!"}


    if __name__ == "__main__":
        startmeup(port=8000)
