
/**
 * serv thrift
 */

// include "types.thrift"

namespace py serv

/**
 * Node struct
 */
struct RemoteNode {
    1:i32 id,
    2:string ip_addr,
    3:i32 port,
}


/**
 * Accept remote calls as a server
 */
service Remote {
    /**
    * A method definition looks like C code. It has a return type, arguments,
    * and optionally a list of exceptions that it may throw. Note that argument
    * lists and exception lists are specified using the exact same syntax as
    * field lists in struct or exception definitions.
    */

    // oneway
    bool ping(),

    RemoteNode find_successor_r(1:i32 id),

    // oneway
    void set_predecessor(1:RemoteNode node),

    void update_finger_r(1:RemoteNode node, 2:i32 index)

    RemoteNode successor_r(),

    RemoteNode predecessor_r(),

    RemoteNode closest_preceding_node_r(1:i32 id),

    // oneway
    void notify_r(1:RemoteNode node),

    i32 id_r(),

    string ip_r(),

    i32 port_r(),

    void rpc_test(1:string test_str),


    // define Node structure
    // Node getRemoteNode(),

    /**
     * This method has a oneway modifier. That means the client only makes
     * a request and does not listen for any response at all. Oneway methods
     * must be void.
     */
    // oneway void zip()

}