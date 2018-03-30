# microBlockchain
![#4b0d89](https://placehold.it/15/4b0d89/000000?text=+) `µBlockchain` - a training project to grasp Blockchain's basic concepts.

This projet is an incentive to learn how Blockchain works.
To train on Python3.6 basic concepts and basic HTTP requests.
And to make a minimalist Blockchain toolkit to try new features and experiments.

This project has been built following over [Daniel val Flymen](https://github.com/dvf)'s tutorial: [Learn Blockchain by building one](https://hackernoon.com/learn-blockchain-by-building-one-117428612f46).
That's why I strongly advise you to follow along the tutorial, and check [his repository](https://github.com/dvf/blockchain) and his tutorial for further information

## Dependencies & Installation

You need:
* Python3.6
* pipenv
* Flask
* requests

1. Install Python3.6+
1. Intall pipenv
1. Install the tutorial's dependencies

## Basic usage

To use the µBlockchain:

1. Install dependencies
1. Clone the repository
1. Run blockchain.py using
`python3.6 blockchain.py`
1. Once running you can
	* See the whole chain
	`bash see_chain.sh`
	* Make a transaction
	`bash see_chain.sh sender recipient amount`
	example:
	`bash see_chain.sh satan me 666`
	* Mine on the µBlockchain
	`bash mining.sh`
	
Have fun! :)


I'd like to thank @dvf for this absolutely minimalistic and yet concise tutorial, waiting for updates :)




## TODO: 
- [x] Implement Consensus algorithms
- [ ] Fix bash scripts bugs with strings params
- [ ] Test consensus algorithms and routes *(use a different port and a different machine)* and bash scripts
- [ ] Clean code
- [ ] Add more features
- [ ] Test
- [ ] Create middleware modules
- [ ] Test
- [ ] Create a "micro" React Web app to visualize how the block chain is created and how it is constructed through nodes interactions between nodes
- [ ] Test
- [ ] Install [Popmotion](https://github.com/Popmotion/popmotion) to create beautiful animations
