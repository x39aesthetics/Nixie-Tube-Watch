//New Blink.c

#define F_CPU 1000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

uint8_t digitTable[10] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09};
uint32_t dsecs;
dsecs = 0;


#define DIGIT_SELECT_B	0x0F  // 00001111, pins 0 through 3 of port B are outputs
#define TUBE_SELECT_D	0xF0  // 11110000, pins 4 through 7 of port D are outputs

void display(unsigned char, unsigned char, unsigned char, unsigned char, unsigned char);

ISR (TIMER1_OVF_vect) {
	dsecs++;
	if(dsecs == 864000){
		dsecs = 0;
	}
	TCNT1 = 15536;
}

int main(void) {
	
	DDRB |= DIGIT_SELECT_B;
	DDRD |= TUBE_SELECT_D;
	unsigned char minsOne;
	unsigned char minsTen;
	unsigned char secsOne;
	unsigned char secsTen;
	unsigned char hrsOne;
	unsigned char hrsTen;
	uint8_t ignite = 0xff;
	
	TCNT1 = 15536
	TIMSK1 = (1 << TOIE1);
	sei();
	while (1) {
		
		
		
		secsOne = ((dsecs - dsecs%10)/10) % 10;
		secsTen = ((dsecs - dsecs%10)%60 - secsOne) / 10;
		minsOne = ((dsecs - dsecs%600))

	}
	return 0;
}

void display(unsigned char tube0, unsigned char tube1, unsigned char tube2, unsigned char tube3, unsigned char isOn) {
	//write the digital outputs to the decoder chip, then output values to select which tube turns on
	//
	PORTB = digitTable[tube0];
	PORTD = 0x10 & isOn;
	_delay_ms(2);
	PORTD = 0x00;
	_delay_ms(4);
	PORTB = digitTable[tube1];
	PORTD = 0x20 & isOn;
	_delay_ms(2);
	PORTD = 0x00;
	_delay_ms(4);
}
