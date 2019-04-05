/* Checks VCF data entries for unexpected formats, printing them to stdout. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <regex.h>


int main(int argc, char **argv)
{
  /* Regex */
  regex_t regex;
  int reti;
  char msgbuf[100];

  /* Compile regular expression */
  reti = regcomp(&regex, "^[0-9][|][0-9]$|^[.]$", REG_EXTENDED);
  if( reti ){ fprintf(stderr, "Could not compile regex\n"); exit(1); }

  /* Read from stdin */
  int k = 0, t;
  char *entry;
  char *line = NULL;
  size_t size, n;
  while((n = getline(&line, &size, stdin)) != -1)
  {
    if(line[0] == '#') continue;
    entry = strtok(line, "\t");

    /* Skip the first nine columns */
    for(int j = 0; j < 9; j++) {
      entry = strtok(NULL, "\t");
    }

    /* Read entries */
    t = 0;
    while(entry != NULL)
    {
      /* Execute regular expression */
      reti = regexec(&regex, entry, 0, NULL, 0);
      if( !reti ){
        ; /* Pass */
      }
      else if( reti == REG_NOMATCH ){
        printf("%s\n", entry);
      }
      else{
        regerror(reti, &regex, msgbuf, sizeof(msgbuf));
        fprintf(stderr, "Regex match failed: %s\n", msgbuf);
        exit(1);
      }

      /* Free compiled regular expression to use regex_t again */
      regfree(&regex);

      /* Get next entry */
      entry = strtok(NULL, "\t");
      t++;
    }
    k++;
  }

  if(line) free(line);
  return 0;
}
