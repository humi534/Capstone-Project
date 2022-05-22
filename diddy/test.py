import Path

path = Path.Path([[(1,1),"straight"], [(1,2), "straight"], [(1,3), 'scan']])
print(path.toString())
print(path.getCurrentPosition())
path.updatePosition((1,1))
print(path.getOrderFromPosition((1,3)))

