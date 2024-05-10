import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class KochSnowflake(Node):
    def __init__(self):
        super().__init__('koch_snowflake_bot')
        self.twist_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        self.pose = None
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.cb_pose,
            10)

        self.declare_parameter('speed', 1.0)
        self.declare_parameter('omega', 20.0)

    def cb_pose(self, msg): #Callback function to update the position of the turtle
        self.pose = msg


    def forward(self, distance):    # go straight
        speed = self.get_parameter('speed').get_parameter_value().double_value
        vel_msg = Twist()
        if distance > 0:
            vel_msg.linear.x = speed
        else:
            vel_msg.linear.x = -speed

        # Set other components of the Twist message
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = 0.0

        # Set loop rate
        loop_rate = self.create_rate(100, self.get_clock()) # Hz

        # Calculate time
        T = abs(distance/speed)

       # Publish first msg and note time
        self.twist_pub.publish(vel_msg)  #Turtle started.
        when = self.get_clock().now() + rclpy.time.Duration(seconds=T)  # Set the time when the motion should end

       # Publish msg while the calculated time is up
        while (self.get_clock().now() < when) and rclpy.ok():
            self.twist_pub.publish(vel_msg)  # On its way..
            rclpy.spin_once(self)   # loop rate

       # Set velocity to 0, stop motion
        vel_msg.linear.x = 0.0
        self.twist_pub.publish(vel_msg) # Arrived to destination.


    def turn(self, angle):
        omega = self.get_parameter('omega').get_parameter_value().double_value
        vel_msg = Twist()

        vel_msg.linear.x = 0.0
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0

        if angle > 0:
            vel_msg.angular.z = math.radians(omega)
        else:
            vel_msg.angular.z = math.radians(-omega)

       # Set loop rate
        loop_rate = self.create_rate(100, self.get_clock()) # Hz

       # Calculate time
        T = abs(angle/omega)     # s

       # Publish first msg and note time
        self.twist_pub.publish(vel_msg)
        when = self.get_clock().now() + rclpy.time.Duration(seconds=T) # Calculate time required to complete the turn

       # Publish msg while the calculated time is up
        while (self.get_clock().now() < when) and rclpy.ok():
            self.twist_pub.publish(vel_msg)   # On its way...
            rclpy.spin_once(self)   # loop rate

       # Set velocity to 0
        vel_msg.angular.z = 0.0
        self.twist_pub.publish(vel_msg)


#Koch fractal
    def draw_koch_snowflake(self, order, length): #recursive function to draw koch snowflake
        for _ in range(3):
            self.draw_curve(order, length)
            self.turn(-120)

    def draw_curve(self, order, length):
        if order == 0:
            self.forward(length)
        else:
            for a in [60,-120,60,0]:
                self.draw_curve(order - 1, length / 3)
                self.turn(a)

#Caesaro fractal
    def draw_curve_caesaro(self, order, length, angle):  #recursive function to draw Caesaro fractal
        if order == 0:
            self.forward(length)
        else:
            length = length / (2 + 2 * math.cos(math.radians(angle)))
            self.draw_curve_caesaro(order - 1, length , angle)
            self.turn(angle)
            self.draw_curve_caesaro(order - 1, length , angle)
            self.turn(-angle*2)
            self.draw_curve_caesaro(order - 1, length , angle)
            self.turn(angle)
            self.draw_curve_caesaro(order - 1, length , angle)


    def caesaro(self, order, legnth):
        for _ in range(4):
            self.draw_curve_caesaro(order, legnth,85)
            self.turn(90)

def main(args=None):
    rclpy.init(args=args)

    koch_bot = KochSnowflake()
   #koch_bot.draw_koch_snowflake(3, 4)

    koch_bot.caesaro(1,3) #iteration/order: 1, size/lenght: 3

    rclpy.spin(koch_bot)

    koch_bot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
