import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

/**
 * Created by michellejagelid on 2018-03-03.
 */
public class RPIClient {

    private float temperature;
    private float humidity;

    public RPIClient(String hostname, int port){
        connect(hostname, port);
    }

    /** Connect a client to a server with hostname and port given as arguments. */
    private void connect(String hostname, int port){
        try {
            // Make connection and get input and output stream of the socket.
            Socket s = new Socket(hostname, port);
            PrintWriter out = new PrintWriter(s.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
            Boolean done = false;

            // poll server for values every 60 seconds
            while (!done) {
                out.write("ready");                // Tell server to send data
                String read = in.readLine();       // read data check that not null, wait until data read.
                while (read == null){              // wait until server sends a respond. Busy wait, kinda ugly.
                    read = in.readLine();
                }
                if (read.matches("quit")) {        // Server might send done before it decides to go down or something
                    done = true;
                }else {
                    process(read);
                }
                Thread.sleep(60000);               //delay for 60 seconds
            }

            //Close connection
            s.close();
            System.out.println("Connection closed. Client shutting down.");

        }catch (UnknownHostException e ){System.err.print("Socket:" +  e.getMessage());
        }catch (IOException e){System.err.print("IO: " + e.getMessage());
        }catch (InterruptedException e){System.err.print("Thread interrupted during sleep: " + e.getMessage());}
    }

    /** Process the given input from the server. Separate the values and
     * prepare the values for the GUI*/
    private void process(String read){
        String[] values = read.split(" ");      // Assume values separated by space
        if (values.length != 2){                // How many values will we have? 2?
            System.out.println("Missing values from server. Only "+ values.length + " received.");
        }
        //Should probably check that values are in digit format here before we convert.
        temperature = Float.parseFloat(values[0]);
        humidity = Float.parseFloat(values[1]);
    }

    /** Accessible functions for GUI*/
    public float getTemperature(){
        return temperature;
    }

    public float getHumidity() {
        return humidity;
    }
}
