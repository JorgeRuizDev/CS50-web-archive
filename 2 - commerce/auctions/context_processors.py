from . import util


def watchlist_count(request):
    watchlist_size = len(util.obtain_watchlist(request.user))
    return {"watchlist_size": watchlist_size}
