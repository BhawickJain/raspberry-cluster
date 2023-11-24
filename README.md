# Raspberry Pi Super Computer Cluster

- [ ] Motivation?
  - [Why would you build a Raspberry Pi Cluster?](https://www.youtube.com/watch?v=8zXG4ySy1m8)
  - [blog](https://www.jeffgeerling.com/blog/2021/why-build-raspberry-pi-cluster)

- [ ] use HPC job management software like SLURM
  - [Parallel Computing with Python on a Raspberry Pi Cluster - OpenMPI and mpi4py install](https://www.youtube.com/watch?v=caXD_6JMXfA)
  - [Python Simulations with SLURM](https://www.youtube.com/watch?v=iJnuLnPeoj8)
- [ ] host a site or a service that performs a service much cheaper than a cloud service
- [ ] perform parallelised math problem jobs
- [ ] manage a NAS drive
- [ ] isolated linux computer, it won't matter if I break it
- [ ] node clusters to serve a function


- [ ] Is this a super computer or a just a compute cluster?

- [Python and SLURM](https://www.youtube.com/watch?app=desktop&v=4lKcou1-3OY)

- 2 x 35.00 [Raspberry Pi 4 Model B - 2GB](https://www.ebay.co.uk/itm/404593051397?hash=item5e33a00705:g:HDIAAOSw-o9lQ6lb&amdata=enc%3AAQAIAAAAwHEosaBESy1JFxpl6PKudeJkcvaXN9vvMQMM%2BeJbMpz8Z%2BQ%2F6XclW16pArmxERKuTTImPDmMrBI7bfetDYy%2Fzr5s53CwR3tnMmyOsVZBURaW1UGHDkUMJJ3P8FzDG6jkHH6hrdZkKEACnJfCJGTC3XFLv1oyiLi%2FbJcYpa4P7h0G34NY%2FQcd%2FgzvtSk4RtIxjfmaCQT%2B1NnsZCHAmmlaTvbwf6hRYff8xGZNlRKj%2BgyqPHgOqnQvjvVWZUNAgEm55w%3D%3D%7Ctkp%3ABk9SR9aLh52AYw)
- 0 x 27.00 [Network Switch Router with PoE 40W budget](https://www.amazon.co.uk/TP-Link-Switch-Gigabit-Surveillance-TL-SG1005LP/dp/B08D9G7WPN/ref=mp_s_a_1_3?crid=15MFIC8Q9809A&keywords=network+switch+poe&qid=1700842288&sprefix=network+switch+poe%2Caps%2C122&sr=8-3)
- 1 x 30.00 [Tenda 5 port, 4PoE 63W buget](https://www.amazon.co.uk/Tenda-Desktop-Overload-Protection-TEG1105P-4-63W-TEG1105P-4-63W-UK/dp/B09CYBMK51/ref=psdc_430573031_t1_B08D9G7WPN?th=1)
- 2 x 18.40 [Raspberry Pi POE HAT Power Over Ethernet Revision3 3b+ 4b NEW rev3 UK Official](https://www.ebay.co.uk/itm/404458855152?hash=item5e2ba05af0%3Ag%3AGSkAAOSwlhtj57vd&amdata=enc%3AAQAIAAAA4NFRpjRWUSkAUGxXcuIhZlbSB8P1N3V7x5QS6bdriL0YHpY7H0rgtlLiEl9n1ycQomx0zlCWGOwvnJiqHHlG6c8kqDApLxM1UV4dkBy3cJmHN0TTT5ikASKMzRz5yl1q7E%2B6jEXClfHiPgyQkwftIF2cUOy7YpL22eN8rDqFF55iADHlnbvwVVVCb4gMfGPzqhckCQdGh%2FVS9gIrPeyzvjq8i2pTH%2BFMNX9WO4sidBXcAdItAR76v3IuOP19oyuyvwkdYFxWE1t4VAfTS2X4%2BWsPSIC3bDQajvjLozQYxhQ1%7Ctkp%3ABk9SR7bTsq-AYw&LH_BIN=1)
- 1 x 20.00 [Rack](https://www.amazon.co.uk/GeeekPi-Raspberry-Cluster-Heatsink-Stackable/dp/B07Z4GRQGH/ref=mp_s_a_1_17?crid=3DNY462ZTWU7W&keywords=raspberry%2Bpi%2Bshelf%2Brack&qid=1700837729&sprefix=raspberry%2Bpi%2Bshelfrack%2Caps%2C90&sr=8-17&th=1&psc=1)
  - should be able to accomodate the PoE switch but unlikely will fit an additional cooling fan
- [ ] find microsd cards
- [ ] find all rj45 cables

## Build Plan
__strictly optional__
- 3 x [RJ45 cables of unknown length with PoE](https://www.amazon.co.uk/StarTech-com-50cm-CAT6-Ethernet-Cable/dp/B0080OTEGE/ref=sr_1_3?crid=8YTYRQFNWSTI&keywords=RJ45+cable+PoE&qid=1700842466&refinements=p_n_feature_twelve_browse-bin%3A90876406031&rnid=90876402031&s=computers&sprefix=rj45+cable+poe%2Caps%2C105&sr=1-3)


## Build Plan

- [ ] create a build plan to make it certain how exactly you will build and use it.
- [Raspberry Pi Cluster Ep 1 - Introduction to Clustering](https://www.youtube.com/watch?v=kgVz4-SEhbE)
- [How to build a Raspberry Pi Cluster - SLURM Cluster Config](https://www.youtube.com/watch?v=l5n62HgSQF8)
- [instructions](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa3Z2Qkg3V2MwZGxhMUxfc1hBWm9WZGNzMWx4Z3xBQ3Jtc0trbHRxZmxPcTh1eUdXd1RUNEhCM1daWEhPY0JuaHlsUjYwYVJCYldzVkN4aHI5dEFzRmNVZGhtRDZfdHBlN0E4Y0RYNHc4OFlwRUVRc1d6Y2g1OWdHd2xxTGg3ODlaZ0JJSWU1NVRFRE5yZWhKRWozYw&q=https%3A%2F%2Fglmdev.medium.com%2Fbuilding-a-raspberry-pi-cluster-aaa8d1f3d2ca&v=iJnuLnPeoj8)
- Gareth Mills articles: 
  - [Part I](https://glmdev.medium.com/building-a-raspberry-pi-cluster-784f0df9afbd)
  - [Part II](https://glmdev.medium.com/building-a-raspberry-pi-cluster-aaa8d1f3d2ca)
  - [Part III](https://glmdev.medium.com/building-a-raspberry-pi-cluster-f5f2446702e8)

### Parts

- [raspberry pi 4 model b, 2gb](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/): ideally 4 gb but its double the price, ideally Pi 5 but that's astronomical for current project scope
- [poe hat](https://www.raspberrypi.com/products/poe-hat/): enables pi's to be powered via ethernet, significantly reducing material and clutter with a minor penality on clock speed (1.5GHz instead of 1.8GHz) `[ref needed]`
  - [additional details](https://www.raspberrypi.com/news/announcing-the-raspberry-pi-poe-hat/)

### Assembly

### Software Setup


### 
