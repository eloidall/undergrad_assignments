#ifndef DB_H
#define DB_H

#define max_length_comment 64
#define max_length_handle 32

// Needed in header file or only in .c ??
#define initial_capacity 4


// Define both structures

typedef struct Record {
	char handle[max_length_handle];
	unsigned long followers_count;
	char comment[max_length_comment];
	unsigned long date_last_modified;
} Record;


typedef struct Database {
	Record *data;
	int capacity;
	int size;
} Database;


// Function prototypes

Database db_create();

void db_append(Database * db, Record const * item);

Record * db_index(Database * db, int index);

Record * db_lookup(Database * db, char const * handle);

void db_free(Database * db);

void db_load_csv(Database * db, char const * path);

void db_write_csv(Database * db, char const * path);

#endif
