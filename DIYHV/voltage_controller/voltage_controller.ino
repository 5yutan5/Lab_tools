const int PWM_PIN = 6; // define pin 6 speed
const int L = 4;       // define pin 5 for B1B
const int R = 5;       // define pin 5 for B1B
const int D = 9;       // high frequency switching
// change this: this is test for 2 minutes
const int CYCLE1 = 30;
const int CYCLE2 = 120;
const int CYCLE3 = 600;
const int CYCLE4 = 3000;
const int CYCLE5 = 6000;
const int CYCLE6 = 12000;
// change this: this is test for 2 minutes end

void setup()
{
    Serial.begin(9600);
    pinMode(PWM_PIN, OUTPUT);
    pinMode(L, OUTPUT);
    pinMode(R, OUTPUT);
    pinMode(D, OUTPUT);
    delay(3000);
}
void loop()
{
    Serial.println("please input your command");
    delay(1000);
    switch (Serial.read())
    {
    case 'a':
        run_static(44);
        break;
    case 'b':
        run_static(100);
        break;
    case 'c':
        run_static(255);
        break;
    case 'v':
        run_static(0);
        break;
    case 'd':
        run_dynamic(44, CYCLE1, 2000);
        break;
    case 'e':
        run_dynamic(44, CYCLE2, 500);
        break;
    case 'f':
        run_dynamic(44, CYCLE3, 100);
        break;
    case 'g':
        run_dynamic(100, CYCLE1, 2000);
        break;
    case 'h':
        run_dynamic(100, CYCLE2, 500);
        break;
    case 'i':
        run_dynamic(100, CYCLE3, 100);
        break;
    case 'j':
        run_dynamic(HIGH, CYCLE1, 2000);
        break;
    case 'k':
        run_dynamic(HIGH, CYCLE2, 500);
        break;
    case 'l':
        run_dynamic(HIGH, CYCLE3, 100);
        break;
    case 'm':
        run_dynamic(44, CYCLE4, 20);
        break;
    case 'n':
        run_dynamic(44, CYCLE5, 10);
        break;
    case 'o':
        run_dynamic(44, CYCLE6, 5);
        break;
    case 'p':
        run_dynamic(100, CYCLE4, 20);
        break;
    case 'q':
        run_dynamic(100, CYCLE5, 10);
        break;
    case 'r':
        run_dynamic(100, CYCLE6, 5);
        break;
    case 's':
        run_dynamic(HIGH, CYCLE4, 20);
        break;
    case 't':
        run_dynamic(HIGH, CYCLE5, 10);
        break;
    case 'u':
        run_dynamic(HIGH, CYCLE6, 5);
        break;
    }
}
/////static actuation/////
void run_static(int analog_value)
{
    analogWrite(PWM_PIN, analog_value);
    // fixed point
    digitalWrite(L, LOW);  // do not change
    digitalWrite(R, HIGH); // do not change
    // fixed point
    digitalWrite(D, HIGH); // DEAN Switch for HF
}
/////dynamic actuation/////
void run_dynamic(int analog_value, int cycle_num, int delay_time)
{
    for (int i = 0; i <= cycle_num; i++)
    {
        digitalWrite(D, HIGH);              // DEAN Switch for HF
        analogWrite(PWM_PIN, analog_value); // electric source for LF
        // fixed point
        digitalWrite(L, LOW);  // do not change
        digitalWrite(R, HIGH); // do not change
        // fixed point
        delay(delay_time);
        digitalWrite(D, HIGH);      // DEAN Switch for HF
        digitalWrite(PWM_PIN, LOW); // electric source for LF
        delay(delay_time);
    }
}
