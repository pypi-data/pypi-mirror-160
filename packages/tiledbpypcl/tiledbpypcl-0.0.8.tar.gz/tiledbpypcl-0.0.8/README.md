# TileDB python pcl bindings

### package bringing some classes and functions from pcl into python

#### see https://github.com/davidcaron/pclpy (packaging issues and out-of-date)

#### WIP

#### get from pypi:
``
pip install tiledbpypcl
``
#### temp pypi account:
    - username: ctiledb
    - password: TileDBPCL

#### example currently working (version 0.0.7)

```
import tiledbpypcl
from tiledbpypcl import PointCloudXYZ
from tiledbpypcl.point_types import PointXYZ

cloudXYZ = PointCloudXYZ()
for _ in range(100):
    pt = PointXYZ()   // need to add (float, float, float) constructor for point types
    pt.x = 2.0
    pt.y = 2.0
    pt.z = 2.0
    cloudXYZ.push_back(pt)
    
print(cloudXYZ.points)
```