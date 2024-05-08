igdb: igdb.o database.o
	gcc -g -o igdb igdb.o database.o

igdb.o: igdb.c database.h
	gcc -g -c igdb.c

database.o: database.c database.h
	gcc -g -c database.c
