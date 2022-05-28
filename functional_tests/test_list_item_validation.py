from unittest import skip
from .base import FunctionalTest

class ItemValidationtest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith accidentally submits an empty list item.

        # The home page refreshes, and there is an error message.

        # She tries again with some text, which now works.

        # She decides to submit a second blank list item.

        # She receives a similar warning on the list page.

        # She can correct it by filling some text in.

        self.fail("To be written")
