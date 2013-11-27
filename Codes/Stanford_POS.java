/*
 * This code is used to tag a tweet's part of speech by Stanford POS Tagger
 * the package is downloaded for the website http://nlp.stanford.edu/downloads/tagger.shtml
 */
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

import edu.stanford.nlp.tagger.maxent.MaxentTagger;
 
public class Stanford_POS 
{
	public static void standfordPOS(String fileName) throws IOException
	{
		// Initialize the tagger
		MaxentTagger tagger = new MaxentTagger("taggers/english-left3words-distsim.tagger");
		
		//input a file
		Scanner inFile = new Scanner(new FileReader(fileName));
		
		//output a file
		FileWriter fileOut = new FileWriter(fileName.split(".txt")[0] + "_POS.txt");		//open file for output
		BufferedWriter outFile = new BufferedWriter(fileOut);
		
		String line  = "";
		
		while(inFile.hasNext())
		{
			line = inFile.nextLine();			
			if(line.split("\t").length > 1)
			{
				outFile.write(line.split("\t")[0] + "\t" + tagger.tagString(line.split("\t")[1]));
				outFile.newLine();
			}
		}
		
		inFile.close();
		outFile.close();
		
		System.out.println(fileName + " job done.");
	}
	
    public static void main(String[] args) throws IOException, ClassNotFoundException 
    {
    	standfordPOS("us_tweets_ipad1.txt");
    	standfordPOS("us_tweets_ipad2.txt");
    	standfordPOS("us_tweets_ipad3.txt");
    	standfordPOS("us_tweets_iphone4s.txt");
    	standfordPOS("us_tweets_iphone5.txt");
    	standfordPOS("us_tweets_kindlefire1.txt");
    	standfordPOS("us_tweets_kindlefire2.txt");
    	standfordPOS("us_tweets_nexus7.txt");
    }
}