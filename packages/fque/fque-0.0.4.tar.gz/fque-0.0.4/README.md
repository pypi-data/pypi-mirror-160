# fque #

## Overview ##

Fast Queue (short fque) is a simplified version of the built-in queue.Queue() with basic functionality but higher
performance. The inspiration behind this library is to have a highly performant queue that allows inter-thread 
communication with high throughputs.

fque runs 10x faster than the standard queue implementation by relying on pythons built-in deque and
implementing just the minimum needed locks.

## Usage ##
The library can be directly installed from pypi
```angular2html
pip install fque
```

The usage resembles queue.Queue() but with just the basic functions needed to share information across threads:
```angular2html
import fque

q = fque.Queue()
q.put(1)
result = q.get()

```

The Queue object accepts a maxsize parameter and the .get() function accepts a block and timeout, same as the 
standard queue.Queue(). The empty and full checkers are also implemented. Other features as the timeouts for 
put are not going to be implemented as they reduce the performance of the queue.

## Licence & Copyright ##

Licensed under the [MIT License](LICENSE).