# Qubes OS Host-based Intrusion Detection System (HIDS)

 This is a custom, lightweight Host Based Intrusion Detection System (HIDS) designed to operate inside isolated Qubes OS VMS. This engine performs real time file integrity Monitoring (FIM) on core system configurations and inspects activity for execution anomalies.

 ##Features 

 * **File Integrity Monitoring (FIM):** Generates cryptographic baseline hashes (SHA-256) for target directories ('/etc') and detects  unauthorized file modifications or deletions.
 * **Suspicious Process Detection:** Leverages 'psutil' to inspect system process trees, flagging binaries running out of untrusted, executable paths like '/tmp'.
 * **Structured Alerting:** Outputs security events in structured JSON format with severity classifications ('HIGH', 'CRITICAL') for streamlined integrations with STEMs or log collectors.

 ## Technical Architecture

* **'fim.py'**: Manages baseline hash storage ('baseline_db.json') and continuously scans target directory trees for checksum drift.
* **'process_monitor.py'**: Queries process table attributes ('pid', 'name'. 'exe') to identify anomalous runtime behavior.
* **'main.py'**: Orchestrates monitoring threads and streams formatted alert outputs every 5 seconds.

 ## Installation & Setup

1. **Clone the Repository**
   '''bash
   git clone [https://github.com/icanttsaveyou/qubes-hids-project.git](https://github.com/icanttsaveyou/qubes-hids-project.git)

2. **Set up Environment**
   '''bash
   python3 -m venv venv
   source venv/bin/activate
   pip install psutil

3. **Running the HIDS Engine**
   '''bash
   cd ~/qubes-hids-project
   source venv/bin/activate
   sudo ./venv/bin/python main.py

4. **Testing Alert Logic**

A. Test File Modification Alert:
   '''bash
   sudo sh -c 'echo "# test" >> /etc/hosts'

B. Test Process Execution Alert:
   '''bash
   cp /bin/sleep /tmp/suspicious_proc && /tmp/suspicious_proc 100 &
