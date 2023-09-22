/*

transforming imported dct coefficients (scaled by 8) and generating
custom compression quantization rate for each 8*8p block based
on that

DCT values lie between -8192 and 8184

*/


#include <stdio.h>
#include <stdlib.h>

#include "adaptf.h"

#include "jinclude.h"


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








