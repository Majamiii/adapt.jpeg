/*

transforming imported dct coefficients (scaled by 8) and generating
custom compression quantization rate for each 8*8p block based
on that

DCT values lie between -8192 and 8184

*/


#include <stdio.h>
#include <stdlib.h>

int num_pixels()        //line counter, reading from txt with dct coefficients
{
    int count = 0;          //number of lines is equal to the number of pixels
    FILE *fp;
    fp = fopen("./build/dctcoefs.txt", "r");
    char c;

    if (fp == NULL)
    {
        printf("Can't open file for reading.\n");
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
    fptr = fopen("./build/modicoefs.txt","a");      //make a file for storing modified coefficients

    FILE *fp;
    fp = fopen("./build/dctcoefs.txt", "r");

    int n;
    float ogcoefs[nofpixels];
    int i = 0;
    int j=0;
    int k=0;
    float sum = 0;
    //changing one block of DCT coefficients

    for (i = 0; i < 64; i++) {          //change 64 later to DCTSIZE2, do this for every pixel
        fscanf(fp, "%f\n", &ogcoefs[i]); //store info in ogcoefs array

        if(ogcoefs[i]<0) {
            ogcoefs[i] = -ogcoefs[i];
        }

        if (i==0) {
            ogcoefs[i] = ogcoefs[i] *1/15;              //diagonally scaling the coefficients (*1/15, 2/15, ... 15/15)
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if ((i==1)||(i==8)) {
            ogcoefs[i] = ogcoefs[i] *2/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if ((i==2)||(i==9)||(i==16)) {
            ogcoefs[i] = ogcoefs[i] *3/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }
        
        else if ((i==3)||(i==10)||(i==17)||(i==24)) {
            ogcoefs[i] = ogcoefs[i] *4/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if ((i==4)||(i==11)||(i==18)||(i==25)||(i==32)) {
            ogcoefs[i] = ogcoefs[i] *5/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }
        
        else if ((i==5)||(i==12)||(i==19)||(i==26)||(i==33)||(i==40)) {
            ogcoefs[i] = ogcoefs[i] *6/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if ((i==6)||(i==13)||(i==20)||(i==27)||(i==34)||(i==41)||(i == 48)) {
            ogcoefs[i] = ogcoefs[i] *7/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if ((i==7)||(i==14)||(i==21)||(i==28)||(i==35)||(i==42)||(i==49)||(i == 56)) {
            ogcoefs[i] = ogcoefs[i] *8/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if ((i==15)||(i==22)||(i==29)||(i==36)||(i==43)||(i==50)||(i==57)) {
            ogcoefs[i] = ogcoefs[i] *9/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if ((i==23)||(i==30)||(i==37)||(i==44)||(i==51)||(i==58)) {
            ogcoefs[i] = ogcoefs[i] *10/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if ((i==31)||(i==38)||(i==45)||(i==52)||(i==59)) {
            ogcoefs[i] = ogcoefs[i] *11/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if ((i==39)||(i==46)||(i==53)||(i==60)) {
            ogcoefs[i] = ogcoefs[i] *12/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if ((i==47)||(i==54)||(i==61)) {
            ogcoefs[i] = ogcoefs[i] *13/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if ((i==55)||(i==62)) {
            ogcoefs[i] = ogcoefs[i] *14/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        else if (i==63) {
            ogcoefs[i] = ogcoefs[i]/15;             
            fprintf(fptr, "%f\n", ogcoefs[i]);
        }

        sum = sum + ogcoefs[i];

        /*if ((i<counter)&&(i<8)) {
            for (j = 0; j=7; j++) {         //first 8 diagonalls
                
                for (k=1; k<=j+1; k++) {
                    ogcoefs[i + j*7] = ogcoefs[i] * k/15;
                    fprintf(fptr, "%f\n", ogcoefs[i]);
                }
            }
            counter = counter + 1;
        }*/

    }

    fclose(fptr);
    fclose(fp);

    float percent;
    percent = sum / 43.69;

    int integer;
    integer = (int)percent;

    return integer;
}

int main()
{

    int pixels = num_pixels();
    //printf("%d\n", heightp);
    FILE * fptr;
    fptr = fopen("./build/modicoefs.txt","w");
    fclose(fptr);

    int percent = one_block(pixels);

    printf("%d\n", percent);

    return 0;
}
