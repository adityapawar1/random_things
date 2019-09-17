package happyNewYear;
import java.awt.AWTException;
import java.awt.Color;
import java.awt.Robot;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;

import javax.swing.KeyStroke;



public class startBot {

	public static void main(String[] args) throws Exception {
		keyType("HAPPY NEW YEAR1");
		//click();
		
		
			
		}
	public static void keyType(String s) throws Exception{
		Robot r = new Robot();
		r.delay(5000);
		r.keyPress(KeyEvent.VK_SHIFT);
		
	for (char a : s.toCharArray()) {
			ppy new year1
		KeyStroke ks = KeyStroke.getKeyStroke(a, 0);
		//System.out.println(ks.getKeyCode());
		int keyCode = ks.getKeyCode();
		//System.out.println(keyCode);
		
		r.keyPress(keyCode);
		r.delay(10);
		r.keyRelease(keyCode);
		
		r.delay(10);
		
			
		
		}
	
	r.keyRelease(KeyEvent.VK_SHIFT);
	r.keyPress(13);
	r.delay(10);
	r.keyRelease(13);
	r.delay(100);
	r.mousePress(InputEvent.BUTTON1_DOWN_MASK);
	r.delay(100);
	r.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
	}
	
	public static void click() throws Exception {
		Robot r1 = new Robot();
		for (int i=0; i<=900; i += 65) {
			Color color1 = r1.getPixelColor(10, i);
			if (color1.getBlue() != 250) {//check if chat is DoNotDisturb
				r1.mouseMove(10, i);
				r1.mousePress(InputEvent.BUTTON1_DOWN_MASK);
				r1.delay(50);
				r.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
				keyType("HAPPY NEW YEAR1");
				System.out.println(i + " true");//if chat is not DoNotDisturb, print true
			}
			else {
				System.out.println(i + " false");//if chat is DoNotDisturb, print false
			}
			r.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
		}
		
		
		
		//System.out.println(color.getBlue());
		
		
		
	}

}
