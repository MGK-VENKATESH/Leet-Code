Description:
You are given a 0-indexed array heights of positive integers, where heights[i] represents the height of the ith building.

If a person is in building i, they can move to any other building j if and only if i < j and heights[i] < heights[j].

You are also given another array queries where queries[i] = [ai, bi]. On the ith query, Alice is in building ai while Bob is in building bi.

Return an array ans where ans[i] is the index of the leftmost building where Alice and Bob can meet on the ith query. If Alice and Bob cannot move to a common building on query i, set ans[i] to -1.

 

Example 1:

Input: heights = [6,4,8,5,2,7], queries = [[0,1],[0,3],[2,4],[3,4],[2,2]]
Output: [2,5,-1,5,2]
Explanation: In the first query, Alice and Bob can move to building 2 since heights[0] < heights[2] and heights[1] < heights[2]. 
In the second query, Alice and Bob can move to building 5 since heights[0] < heights[5] and heights[3] < heights[5]. 
In the third query, Alice cannot meet Bob since Alice cannot move to any other building.
In the fourth query, Alice and Bob can move to building 5 since heights[3] < heights[5] and heights[4] < heights[5].
In the fifth query, Alice and Bob are already in the same building.  
For ans[i] != -1, It can be shown that ans[i] is the leftmost building where Alice and Bob can meet.
For ans[i] == -1, It can be shown that there is no building where Alice and Bob can meet.
Example 2:

Input: heights = [5,3,8,2,6,1,4,6], queries = [[0,7],[3,5],[5,2],[3,0],[1,6]]
Output: [7,6,-1,4,6]
Explanation: In the first query, Alice can directly move to Bob's building since heights[0] < heights[7].
In the second query, Alice and Bob can move to building 6 since heights[3] < heights[6] and heights[5] < heights[6].
In the third query, Alice cannot meet Bob since Bob cannot move to any other building.
In the fourth query, Alice and Bob can move to building 4 since heights[3] < heights[4] and heights[0] < heights[4].
In the fifth query, Alice can directly move to Bob's building since heights[1] < heights[6].
For ans[i] != -1, It can be shown that ans[i] is the leftmost building where Alice and Bob can meet.
For ans[i] == -1, It can be shown that there is no building where Alice and Bob can meet.

 

Constraints:

1 <= heights.length <= 5 * 104
1 <= heights[i] <= 109
1 <= queries.length <= 5 * 104
queries[i] = [ai, bi]
0 <= ai, bi <= heights.length - 1

Python3:
class Solution:
    def leftmostBuildingQueries(self, heights: List[int], queries: List[List[int]]) -> List[int]:
        # List to store the final answers
        result = [-1] * len(queries)
        # Stores the new queries for each building
        new_queries = [[] for _ in range(len(heights))]
        # Monotonic stack to keep the leftmost valid building
        mono_stack = []
        
        # Preprocess the queries
        for i, (a, b) in enumerate(queries):
            if a > b:
                a, b = b, a  # Swap if a > b (ensuring a < b)
            # Direct answer if the height at b is greater than a or they are the same
            if heights[b] > heights[a] or a == b:
                result[i] = b
            else:
                new_queries[b].append((heights[a], i))
        
        # Process buildings from right to left
        for i in range(len(heights) - 1, -1, -1):
            # For each query at the current building i, check the conditions
            for height_a, idx in new_queries[i]:
                # Perform binary search to find the appropriate building
                pos = self.binary_search(height_a, mono_stack)
                if pos != -1:
                    result[idx] = mono_stack[pos][1]
            
            # Maintain the monotonic stack where heights are strictly increasing
            while mono_stack and mono_stack[-1][0] <= heights[i]:
                mono_stack.pop()
            mono_stack.append((heights[i], i))
        
        return result

    def binary_search(self, height: int, mono_stack: List[tuple]) -> int:
        # Binary search in the monotonic stack to find the highest possible position
        left, right = 0, len(mono_stack) - 1
        best_pos = -1
        while left <= right:
            mid = (left + right) // 2
            if mono_stack[mid][0] > height:
                best_pos = mid
                left = mid + 1
            else:
                right = mid - 1
        return best_pos
