# Redis Database Map

## Getting Started

[Redis](https://redis.io/) database was used as project's database. It is a very fast non-relational database. Installation instructions can be found in the link.

## Keys

Redis was orginized as seen bellow:

* Placemark keys.

```
Key: placemark
Value: set
Example usage: smembers placemark
Explanation: Under the placemark key are stored all the placemark's ids.
```
```
Key: placemark:<id>
Value: hash
Example usage: hgetall placemark:<id>
Explanation: Under the placemark:<id> key are stored all the placemark's attributes: point, polygon, population and centroid.
```
```
Key: placemark:<id>:polygon
Value: set
Example usage: smembers placemark:<id>:polygon
Explanation: Under the placemark:<id>:polygon key are stored all the polygon's attributes if existing: parking slots, fixed demand and demand.
```
```
Key: placemark:<id>:polygon:slots
Value: string
Example usage: get placemark:<id>:polygon:slots
Explanation: Under the placemark:<id>:polygon:slots key is stored the number of parking slots for this block.
```
```
Key: placemark:<id>:polygon:demand
Value: list
Example usage: lrange placemark:<id>:polygon:demand 0 -1
Explanation: Under the placemark:<id>:polygon:demand key are  stored the values of real demand per hour for this specific block.
0 key coresponds to 24:00 hours demand,
13 to 13:00 hours demand, etc.
```
```
Key: placemark:<id>:polygon:fixed_demand
Value: list
Example usage: lrange placemark:<id>:polygon:fixed_demand 0 -1
Explanation: Under the placemark:<id>:polygon:fixed_demand key are  stored the values of fixed demand per hour for this specific block.
0 key coresponds to 24:00 hours demand,
13 to 13:00 hours demand, etc.
```

* User keys.

```
Key: users
Value: set
Example usage: smembers users
Explanation: Under the users key are stored all the user's ids.
```
```
Key: users:<id>
Value: hash
Example usage: hgetall users:<id>
Explanation: Under the users:<id> key are stored all the user's attributes: usertype, username, password (hashed).
```