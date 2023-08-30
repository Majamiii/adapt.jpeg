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
    FILE *fp;
    fp = fopen("./dctcoefs.txt", "r");

    
   // int n, j, k;
    int ogcoefs[nofpixels];
    int newcoefs[nofpixels];
    
    int sum = 0;
    //changing one block of DCT coefficients

    for (int i = 0; i < 64; i++) {          //change 64 later to DCTSIZE2, do this for every pixel
        int x = fscanf(fp, "%i\n", &ogcoefs[i]); //store info in ogcoefs array
    }

  
    int brojilac[63];
    int broj;
    int k=0;
    int j=0;
    for (int i=0; i<64; i++, j++) {

        broj = j+1;
        brojilac[i] = broj;

        if(j==k+7) {
            j=j-7;
            k = k+1;
        }

        // printf("%i ", broj);

        newcoefs[i] = ogcoefs[i] * broj / 15;

        //     printf("%i \n", newcoefs[i]);
        
        if (newcoefs[i] < 0) {
            sum -= newcoefs[i];
        }
        else {
            sum += newcoefs[i];
        }
    }

    fclose(fp);

    int percent;
    percent = sum / 43.69;

    printf("%i \n", percent);

    return percent;
}

int block()
{
    int pixels = num_pixels();
    int percent = one_block(pixels);
    
    return percent;
}
