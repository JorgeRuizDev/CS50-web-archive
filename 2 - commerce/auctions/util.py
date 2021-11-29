from .models import Item
from .models import Bid
from typing import List
from .models import User


def asign_max_bid(listings: List[Item]):
    for listing in listings:
        bids = Bid.objects.filter(item=listing.id)
        max_bid: int = 0

        for bid in bids:
            if bid.ammount > max_bid:
                max_bid = bid.ammount

        if max_bid > 0:
            listing.min_bid = max_bid


def get_max_bid(item_id):
    bids = Bid.objects.filter(item=item_id)

    if len(bids) is 0:
        return Item.objects.get(id=item_id).min_bid

    max_bid: int = 0

    for bid in bids:
        if bid.ammount > max_bid:
            max_bid = bid.ammount

    return max_bid


def is_in_watchlist(user: User, item: Item) -> bool:
    print(Item.objects.get(id=item.id))
    print(f"related={Item.objects.get(id=item.id).users_watching.select_related()}")

    if list(Item.objects.get(id=item.id).users_watching.select_related()).__contains__(user):
        return True
    else:
        return False


def obtain_watchlist(user: User):
    if user is None:
        return

    items = Item.objects.all()
    listing = []
    for item in items:
        if list(item.users_watching.select_related()).__contains__(user):
            listing.append(item)

    return listing
