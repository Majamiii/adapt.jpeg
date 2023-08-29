/*

transforming imported dct coefficients (scaled by 8) and generating
custom compression quantization rate for each 8*8p block based
on that

DCT values lie between -8192 and 8184

*/


#include <stdio.h>
#include <stdlib.h>

#include "adaptf.h"

int num_pixels()        //line counter, reading from txt with dct coefficients
{
    int count = 0;          //number of lines is equal to the number of pixels
    FILE *fp;
    fp = fopen("./dctcoefs.txt", "r");
    char c;

    if (fp == NULL)
    {
        fprintf(stderr, "Can't open file for reading.\n");
        exit(-1);
    }
    
    for (c = getc(fp); c != EOF; c = getc(fp))
        if (c == '\n') // Increment count if this character is newline
            count = count + 1;
 
    // Close the file
    fclose(fp);
    
    return count;
}

int pixel_height(int widthp)
{
    int nofpixels = num_pixels();
    int heightp;        //height in pixels
    heightp = nofpixels/widthp;             //heightp 

    //printf("%d\n", nofpixels);
    //printf("%d\n", widthp);
    return heightp;
}

int one_block(int nofpixels)
{   
    FILE *fptr;
    fptr = fopen("./modicoefs.txt","a");      //make a file for storing modified coefficients

    FILE *fp;
    fp = fopen("./dctcoefs.txt", "r");

    
    int n;
    float ogcoefs[nofpixels];
    /*int i = 0;
    int j=0;
    int k=0;*/
    float sum = 0;
    //changing one block of DCT coefficients

    for (int i = 0; i < 64; i++) {          //change 64 later to DCTSIZE2, do this for every pixel
        int x = fscanf(fp, "%f\n", &ogcoefs[i]); //store info in ogcoefs array

        int kurac = 14;     //igor influence

        for(int zbir = 0; zbir<14; zbir++) {

                for (int k=0, j=zbir; j<k; k++, j--) {
                    ogcoefs[k*8+j] *= (zbir+1)/(kurac+1);
                }
        }

        sum += ogcoefs[i];
        fprintf(fptr, "%f\n", ogcoefs[i]);

    }

    fclose(fptr);
    fclose(fp);

    float percent;
    percent = sum / 43.69;

    int integer;
    integer = (int)percent;

    return integer;
}

int block()
{
    int pixels = num_pixels();
    //printf("%d\n", heightp);
    FILE * fptr;
    fptr = fopen("./modicoefs.txt","w");
    fclose(fptr);
    
    int percent = one_block(pixels);

    //printf("%i ", percent);
  
    
    return percent;
}
