/*

transforming imported dct coefficients (scaled by 8) and generating
custom compression quantization rate for each 8*8p block based
on that

DCT values lie between -8192 and 8184

*/


#include <stdio.h>
#include <stdlib.h>

#include "adaptf.h"


int changed_coefs(int index, int num)
{
    //int pixels = num_pixels();
    //int percent = one_block(pixels);

        
    int broj=0;
    int k=0;
    int j=0;
    int scale[64];
    for (int m=0; m<64; m++, j++) {                 //making an array like 1 2 3 4 5 6 7 8 2 3 4 5 6 7 8 9 3 4 5 6 7 8 9 10 ,... so the
                                                    //diagonalls would have the same number to scale the coefs
        scale[m] = j+1;

        if(j==k+7) {
            j=j-7;
            k = k+1;
        }
    }

    float n = num * scale[index];
            
    return n/15;
}





/*
int *all_percentages(int nofpixels)
{   
    //int height = pixel_height();
    FILE *fp;
    fp = fopen("./dctcoefs.txt", "r");

    int nofblocks = nofpixels/64;
    printf("\n blocks: %i \n", nofblocks);

    int percent=0;
    
   // int n, j, k;
    int ogcoefs[nofpixels];
    int newcoefs[nofpixels];
    int block_count;

    int percentages[nofblocks];
    
    for (block_count=0; block_count<nofblocks; block_count++) {         //find rates for every block

        printf("%i ", block_count);
        int sum = 0;
        //changing one block of DCT coefficient

        for (int i = block_count*64; i < block_count*64 + 64; i++) {          //change 64 later to DCTSIZE2, do this for every pixel
            int x = fscanf(fp, "%i\n", &ogcoefs[i]); //store info in ogcoefs array
        }
    
        int broj=0;
        int k=0;
        int j=0;
        for (int i=0; i<64; i++, j++) {

            broj = j+1;

            if(j==k+7) {
                j=j-7;
                k = k+1;
            }

            // printf("%i ", broj);

            newcoefs[i + block_count*64] = ogcoefs[i+block_count*64] * broj / 15;

            //printf("%i \n", newcoefs[i+ block_count*64]);
            
            if (newcoefs[i+block_count*64] < 0) {
                sum -= newcoefs[i+block_count*64];
            }
            else {
                sum += newcoefs[i+block_count*64];
            }
        }

        fclose(fp);

        percent = 50 + sum / 43.69;

        percentages[block_count] = percent;
        printf("%i \n", percentages[block_count]);
    }

    //printf("%i \n", percent);

    return percentages;
}

int *changed_coefs()
{
    int pixels = num_pixels();
    //int percent = one_block(pixels);

    int *n;
    n = all_percentages(pixels);
    
    return n;
}*/


