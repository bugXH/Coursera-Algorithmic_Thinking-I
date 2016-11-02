# LeetCode Dynamic Programming

**Dynamic programming doesn't necessarily mean recursion**

[Climbing Stairs](#climbing-stairs)

[Decode Ways](#decode-ways)

[Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/)

[Maximum Subarray](https://leetcode.com/problems/maximum-subarray/)


## Climbing Stairs
[Problem URL](https://leetcode.com/problems/climbing-stairs/)

Description:

> You are climbing a stair case. It takes n steps to reach to the top.

> Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Since each time it's either 1 or 2 steps. So to reach n steps, there'll be two possibilities:

- at n - 1 steps, take 1 step
- at n - 2 steps, take 2 steps

Assume f(n) represents the result of n steps, the recurrence formula for f(n) should be f(n) = f(n - 1) + f(n - 2)

Solution:
Use an array to store the result for f(n), time O(n), space O(n)
```java
public int climbStairs(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    if (n == 2) return 2;
    int[] result = new int[n + 1];
    result[1] = 1;
    result[2] = 2;
    for (int i = 3; i <= n; i++) {
        result[i] = result[i - 2] + result[i - 1];
    }
    return result[n];
}
```

Since we only need the result of f(n - 2) and f(n - 1), the array is not necessary, time O(n), space O(1):
```java
public int climbStairs(int n) {
    int f1 = 1, f2 = 2;
    if (n == 1) return f1;
    if (n == 2) return f2;
    for (int i = 3; i <= n; i++) {
        int f3 = f1 + f2;
        f1 = f2;
        f2 = f3;
    }
    return f2;
}
```

Or use recursion, time O(n), space O(n):
```java
public int climbStairs(int n) {
    if (n == 1) return 1;
    if (n == 2) return 2;
    int[] table = new int[n + 1];
    table[1] = 1;
    table[2] = 2;
    return helper(n, table);
}

private int helper(int n, int[] table) {
    if (table[n] != 0) return table[n];
    table[n] = helper(n - 1, table) + helper(n - 2, table);
    return table[n];
}
```


## Decode Ways
[Problem URL](https://leetcode.com/problems/decode-ways/)

Description:

> A message containing letters from A-Z is being encoded to numbers using the following mapping:

> 'A' -> 1
> 'B' -> 2
> ...
> 'Z' -> 26
> Given an encoded message containing digits, determine the total number of ways to decode it.

> For example,
> Given encoded message "12", it could be decoded as "AB" (1 2) or "L" (12).

> The number of ways decoding "12" is 2.




