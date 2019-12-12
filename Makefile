# install python dependencies
install:
	sh ./build.sh

# set up docker dev environment
start_docker:
	docker run -it -v ~/Documents/GWU/Code/distributed_system:/home/c/ds_team_proj_chord_dev vibrant_elbakyan/chord

# compile thrift files
compile:
	rm -rf ./gen-py
	thrift -r --gen py *.thrift