using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System.Threading;

public class animationPlayer : MonoBehaviour
{
    Thread mThread;
    public string connectionIP = "127.0.0.1";
    public int connectionPort = 25001;
    IPAddress localAdd;
    TcpListener listener;
    TcpClient client;
    private Animator anim;
    string receivedMotion;
    bool running;

    private void Start()
    {
        anim = gameObject.GetComponent<Animator>();
        ThreadStart ts = new ThreadStart(GetInfo);
        mThread = new Thread(ts);
        mThread.Start();
    }

    private void Update()
    {
        
        if (receivedMotion == "normal")
        {
            Debug.Log("normal");
            anim.Play("face01");
            receivedMotion = "IDLE";
        }

        if (receivedMotion == "folder")
        {
            Debug.Log("folder");
            anim.Play("body");
            receivedMotion = "IDLE";
        }

        if (receivedMotion == "time")
        {
            Debug.Log("time");
            anim.Play("face02");
            receivedMotion = "IDLE";
        }
    }

    void GetInfo()
    {
        localAdd = IPAddress.Parse(connectionIP);
        listener = new TcpListener(IPAddress.Any, connectionPort);
        listener.Start();

        client = listener.AcceptTcpClient();

        running = true;
        while (running)
        {
            SendAndReceiveData();
        }
        listener.Stop();
    }

    void SendAndReceiveData()
    {
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];

        //---receiving Data from the Host----
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize); //Getting data in Bytes from Python
        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead); //Converting byte data to string

        if (dataReceived != null)
        {
            //---Using received data---
            
            receivedMotion = dataReceived; //<-- assigning receivedPos value from Python
            print("received the motion");

            //---Sending Data to Host----
            byte[] myWriteBuffer = Encoding.ASCII.GetBytes("python file received"); //Converting string to byte data
            nwStream.Write(myWriteBuffer, 0, myWriteBuffer.Length); //Sending the data in Bytes to Python
        }
    }

    
}