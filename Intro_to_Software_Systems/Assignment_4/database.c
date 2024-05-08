// COMP 206 - Assignment 4
// Author: Éloi Dallaire

#include "database.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>



// Creates new db
Database db_create (){
	
	Database db;
	
	// Initialize with proper values
	db.data = malloc(4 * sizeof(Record));
	db.capacity = 4;
	db.size = 0;
	
	return db;
}


// Copies record pointed by item to end of db
void db_append (Database * db, Record const * item){

	// Check if need to reallocate capacity
	if (db->size >= db->capacity) {
		db->capacity *= 2;
		db->data = realloc(db->data, db->capacity * sizeof(Record));
	}

	// Copy record to end of db
	db->data[db->size++] = *item;
}



// Returns pointer to 1st item in db whose handle is given value	
Record * db_index(Database * db, int index){
	
	// Check if valid index
	if (index >= db->size || index < 0) {
		fprintf(stderr, "Error: index provided is out of bounds.\n");
		return NULL;
	}
	// Return found pointer
	return &(db->data[index]);
}


// Returns pointer to 1st item in db whose handle is given value
Record * db_lookup (Database * db, char const * handle){
	
	// Iterate every records in db
	for (int i = 0; i < db->size; i++) {

		Record *record = db_index(db, i);
		// Compare with handle of current record
		if (strcmp(record->handle, handle) == 0) {
			// Match
			return record;
		}
	}
	// No match
	//fprintf(stderr, "Error: handle provided does not exist.\n");
	return NULL;
}


// Releases memory held by underlying array
void db_free( Database * db){
	
	free(db->data);
}



// Helper function: Parses a single line of CSV data into one Record
Record parse_record(char const *line) {
	
	// Create mutable copy of line
	char copy_line[strlen(line + 1)];
	strcpy(copy_line, line);

	Record record;
	
	// Strips on ','
	char *token = strtok(copy_line, ",");
	
	// Copy each fields to proper format
	strncpy(record.handle, token, 32);
	token = strtok(NULL, ",");
	
	record.followers_count = strtoul(token, NULL, 10);
	token = strtok(NULL, ",");

	strncpy(record.comment, token, 64);
	token = strtok(NULL, ",");

	record.date_last_modified = strtoul(token, NULL, 10);
	
	// Return record
	return record;
}



// Append record read from file at path
void db_load_csv ( Database * db, char const * path ){
	
	FILE *file = fopen(path, "r");

	// Buffer
	char *line = NULL;
	size_t size;
	
	// Read each line and append to db
	while (getline(&line, &size, file) != -1) {
		
		// Remove trailing \n
		if (line[strlen(line) - 1] == '\n') {
			line[strlen(line) - 1] = '\0';
		}
		
		// Append each line as a record in db
		Record record = parse_record(line);
		db_append(db, &record);
	}
	
	// Free buffer and close file
	free(line);
	fclose(file);
} 


// Overwrites file at 'path' with content of 'db'
void db_write_csv (Database * db, char const * path ){

	FILE *file = fopen(path, "w");

	// Writes every record from db into csv
	for (int i = 0; i < db->size; i++) {
		Record *record = db_index(db, i); 
		fprintf(file, "%s,%lu,%s,%lu\n", record->handle, record->followers_count, record->comment, record->date_last_modified);
	}
	fclose(file);
}


/*
void main(){

}

*/

