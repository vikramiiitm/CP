''' Koko Eating Bananas

Problem:
Koko has n piles of bananas. The ith pile has piles[i] bananas.
She has h hours to eat all the bananas. Each hour, she chooses one pile
and eats k bananas from it. If the pile contains fewer than k bananas,
she eats all of them and spends the entire hour on that pile.

Return the minimum integer k such that Koko can eat all bananas within h hours.

Example:
Input: piles = [3,6,7,11], h = 8
Output: 4
'''


class KokoEatingBananas:

    def min_eating_speed(self, piles, h) -> int:
        left, right = 1, max(piles)

        while left <= right:
            mid = left + (right - left) // 2

            hours = 0
            for pile in piles:
                hours += (pile + mid - 1) // mid

            # mid is fast enough; try a smaller speed.
            if hours <= h:
                right = mid - 1
            else:
                left = mid + 1

        return left


piles = [3, 6, 7, 11]
h = 8

koko = KokoEatingBananas()
print("Minimum eating speed:", koko.min_eating_speed(piles, h))
