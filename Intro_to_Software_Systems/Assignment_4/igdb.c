#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>

#include "database.h"

#define max_length_comment 64
#define max_length_handle 32



// Helper functions

// Print record with proper format
void print_record(Record *record) {
	struct tm *tm_info;
    	char time_buffer[26];
    	tm_info = localtime(&(record->date_last_modified));
    	strftime(time_buffer, 26, "%Y-%m-%d %H:%M", tm_info);

    	printf("%-35s | %-12lu | %-19s | %-64s\n", record->handle, record->followers_count, time_buffer, record->comment);
}


// Handle error on user input
bool is_valid_input(ssize_t nread) {
	if (nread == -1) {
        	printf("Error reading input\n");
        	return false;
    	}
    	return true;
}


// Trim user input trailing char
void trim_trailing_newline(char *str, ssize_t nread) {
	if (str[nread - 1] == '\n') str[nread - 1] = '\0';
}


// Checks validity of handle
bool is_valid_handle(const char *handle) {
	
	// Checks proper length
    	size_t handle_len = strlen(handle);
    	if (handle_len > max_length_handle) {
        	printf("Error: handle too long.\n");
        	return false;
    	}
	
	// Checks that start with @
	if (handle[0] != '@') {
		printf("Error: handle must start with '@'.\n");
		return false;
	}

	// Checks presence of illegal char
    	for (size_t i = 0; i < handle_len; i++) {
        	if (handle[i] == ',') {
            		printf("Error: handle cannot contain commas.\n");
            		return false;
        	}
    	}
    	return true;
}

// Checks validity of follower count
bool is_valid_follower(const char *followers_str) {
    	
	// Checks proper type
	char *endptr;
	unsigned long followers = strtoul(followers_str, &endptr, 10);
    	if (*endptr != '\0') {
        	printf("Error: followers count must be an integer\n");
        	return false;
    	}
    	return true;
}


// Checks validity of comment
bool is_valid_comment(const char *comment) {
    	
	// Checks proper length
    	size_t comment_len = strlen(comment);
    	if (comment_len > max_length_comment) {
        	printf("Error: comment too long.\n");
        	return false;
    	}

	// Checks for illegal characters
    	for (size_t i = 0; i < comment_len; i++) {
        	if (comment[i] == ',' || comment[i] == '\n' || comment[i] == '\0') {
            		printf("Error: comment contains illegal characters.\n");
            		return false;
        	}
    	}
    	return true;
}


// User interactions
int main_loop(Database *db) {

	// Saved changes flag
    	bool saved_changes = true;

	while (1) {
		
		// Initialize all inputs and parameters
    		char *command = NULL;
		size_t command_size = 0;
	
		char *comment = NULL;
		size_t comment_size = 0;

		ssize_t nread;
		char *token;

		char *operation = NULL;
		char *handle = NULL;
		char *followers_str = NULL;
		char *extra_token = NULL;		
	
		// Get user input
        	printf("> ");
		fflush(stdout);
        	nread = getline(&command, &command_size, stdin);
		
                // Checks validity of input
                if (!is_valid_input(nread)) break;
                
		// Trim trailing newline
                trim_trailing_newline(command, nread);


		// Split input string based on space
		token = strtok(command, " ");
		
		// Parse tokenized input
		while (token != NULL) {
			
			// Ignore consecutive spaces if any
			if (*token != '\0') {

				// Assign value to parameters based on their position
				if (operation == NULL) operation = token;
				else if (handle == NULL) handle = token;
				else if (followers_str == NULL) followers_str = token;
				else if (extra_token == NULL) extra_token = token;
			}
			// Get next token	
			token = strtok(NULL, " ");
		}
		

		// Handle commands based on operation type		        	

		// 1: list
		// Prints out whole db as a table
		if (strcmp(operation, "list") == 0) {
			
			// Checks # of parameters (1)
			if (handle != NULL) {
				printf("Error: unexpected additional parameter.\n");
				continue;
			}

			// Execute operation
            		printf("HANDLE                              | FOLLOWERS    | LAST MODIFIED       | COMMENT                                                   \n");
            		printf("-------------------------------------------------------------------------------------------------------------------------------------\n");
            		for (int i = 0; i < db->size; i++) {
                		print_record(&db->data[i]);
            		}
			continue;
        	}
		

		// 2: add
		// Appends new entry to db
        	else if (strcmp(operation, "add") == 0) {
            	
			// Checks # of arguments (3)
			if (handle == NULL || followers_str == NULL) {
				printf("Error: usage: add HANDLE FOLLOWERS\n");
				continue;
			}
			if (extra_token != NULL) {
				printf("Error: unexpected additional parameter.\n");
				continue;
			}
			
            		// Checks handle validity
            		if (!is_valid_handle(handle)) continue;
	
            		// Checks follower count validity
            		if (!is_valid_follower(followers_str)) continue;

			// Checks if handle already exists
            		if (db_lookup(db, handle) != NULL) {
                		printf("Error: handle '%s' already exists.\n", handle);
                		continue;
            		}
	

            		// Ask for comment
            		printf("Comment > ");
			nread = getline(&comment, &comment_size, stdin);
			
			// Checks validity of input
			if (!is_valid_input(nread)) break;

			// Trim trailing newline		
			trim_trailing_newline(comment, nread);

			            		
			// Checks comment validity
			if (!is_valid_comment(comment)) continue;

            		// All checks passed: execute new entry
            		Record new_record;
            		
			strcpy(new_record.handle, handle);
            		
			unsigned long followers = strtoul(followers_str, NULL, 10);
			new_record.followers_count = followers;
			
            		strncpy(new_record.comment, comment, sizeof(new_record.comment) - 1);
            		
			time_t current_time;
			time(&current_time);
			new_record.date_last_modified = current_time;
            
			// Append to db
            		db_append(db, &new_record);
            		printf("Record added successfully.\n");
            
			// Update changes tracker
            		saved_changes = false;
			continue;
        	}



		// 3: update
        	// Updates existing entry based on handle
        	else if (strcmp(operation, "update") == 0) {
            
                        // Checks # of parameters (3)
                        if (handle == NULL || followers_str == NULL) {
                                printf("Error: usage: update HANDLE FOLLOWERS\n");
                                continue;
                        }
			if (extra_token != NULL) {
				printf("Error: unexpected additional parameter.\n");
                                continue;
                        }
			

                        // Checks handle validity
                        if (!is_valid_handle(handle)) continue;

                        // Checks follower count validity
                        if (!is_valid_follower(followers_str)) continue;

                        // Checks if handle already exists
			Record *record = db_lookup(db, handle);
			if (record == NULL) {
                                printf("Error: No entry with handle '%s.\n", handle);
                                continue;
                        }

			
                        // Ask for comment
                        printf("Comment > ");
                        nread = getline(&comment, &comment_size, stdin);

                        // Checks validity of input
                        if (!is_valid_input(nread)) break;

                        // Trim trailing newline
                        trim_trailing_newline(comment, nread);

                        // Checks comment validity
                        if (!is_valid_comment(comment)) continue;


            		// All checks passed: execute update
            		unsigned long followers = strtoul(followers_str, NULL, 10);
			record->followers_count = followers;
            		
			time_t current_time;
            		time(&current_time);
            		record->date_last_modified = current_time;
            		
			strncpy(record->comment, comment, sizeof(record->comment));
            		printf("Record updated successfully.\n");
            		
			// Update saved changes tracker
			saved_changes = false;
			continue;
        	}


		// 4: save
		// Writes db to database.csv
		else if (strcmp(operation, "save") == 0) {
            		
			// Checks # of parameters (1)
			if (handle != NULL) {
				printf("Error: unexpected additional parameter.\n");
				continue;
			}

			// Execute operation
			db_write_csv(db, "database.csv");
			printf("Changes saved.\n");
			saved_changes = true;
			continue;
		}

		// 5: exit force
		// Quits program
		else if ( strcmp(operation, "exit") == 0 && handle != NULL ) {
				
			// Checks # of parameters (2)
			if (followers_str != NULL) {
				printf("Error: unexpected additional parameters.\n");
				continue;
			}
			// Quit program
			if (strcmp(handle, "fr") == 0) {
				break;
			}
			else {
				printf("Error: usage: exit fr.\n");
				continue;			
			}
		}


		// 6: exit
		// Quits program
		else if (strcmp(operation, "exit") == 0) {

			// Sends warning if unsaved changes
			if (!saved_changes) {
				printf("Error: you did not save your changes. Use 'exit fr' to force exiting anyway.\n");
				continue;
			}
			
			// Exit if changes were saved
			break;
        	}     
		

		// 7: Unsupported command
                else {
			printf("Error: Unknown command.\n");
			continue;
		}

	// Ends program with success
	return 0;
	}
}



int main() {
	Database db = db_create();
	db_load_csv(&db, "database.csv");
	return main_loop(&db);

}

