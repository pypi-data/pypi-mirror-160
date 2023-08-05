# FlowhHash

A generic python3 hashing algorythm where the input is executed as control flow instructions.

The way that the hash combines values together is definable by the user and partially determines the security of the hash.

Always test yourself if you use a different hash combiner other than the default.

## Info

This repository exists to document the algorithm and tests is validity as a hashing algorithm.

The implimentation provided is not meant to be efficient, and as it is currently, it is not.

This sadly does mean as of right now (07-14-2022) certain tests of the algorithm will not adequately demonstrait its security.

There are future plans to define a more efficient implementation in another language.

## Tests

Due to the performance limitations detailed above, the following tests do not operate on inputs longer than 128. (4096 bytes using 256 bit chunks)

### Pattern Destruction Testing

Chi squared testing of patterned input against a discrete uniform distribution yields inconclusive but promising results.

The p-values are: [
    0.05, 0.05, 0.075, 0.1, 0.1, 0.1, 0.1, 0.15,
    0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3,
    0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.5, 0.5,
    0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.7, 0.7,
    0.7, 0.8, 0.8, 0.8, 0.9, 0.9, 0.95, 0.98
] for `iter = 64`.

And whilst it is promising that the best significance level for rejecting the safety of the algorithm is 5% especially given the quantity of tests;
We should be first assumming that the algorithm is not safe and using this measure to determine if it is.

Through analysing the actual distributions that are being tested shows no pattern in the resulting hashes, with the exception of `[255]` which produced a preference for `8` (`10` results) modulo `16` over `64` tests; However when tested with more computing power the anomaly disappears.

### Sensitivity Testing

Chi squared testing of subtly different input against a discrete uniform distribution produces consistently adhering results.

This result is unsurprising, but still nesacarry to test the security of the algorithm.

## Story

Hashing algorythms are defined by the following 2 properties:
* All of the input is utilized in the hashing process
* Small changes to the input data will result in wildly different results

I noticed that one way to achive the second property is to let the input determine the flow of the hashing process.
The first property however would require that all data had the ability to change the flow of the hashing process.
This is potentially self destructive, as letting all data change the flow of the hashing process could result in data being skipped over, and hence left out of the hash.

At which point I had the following idea:

What if the act of changing the flow of the hashing process could be used to interact with the data?

This library is an implimentation of that idea using a "mutating goto" that mutates and collects the data that it passes through, incorporating them into the hash.