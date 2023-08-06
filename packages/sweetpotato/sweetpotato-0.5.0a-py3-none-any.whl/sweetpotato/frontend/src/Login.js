import React from "react";
import { Button, Input, Text } from "@ui-kitten/components";
import { View } from "react-native";

export class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <View
        style={{
          justifyContent: "center",
          alignItems: "center",
          width: "100%",
          flex: 1,
        }}
      >
        <View
          style={{
            flexDirection: "row",
            marginTop: 4,
            width: "100%",
            justifyContent: "center",
          }}
        >
          <Input
            placeholder={"Username"}
            value={this.state.username}
            onChangeText={(text) => this.setUsername(text)}
          />
        </View>
        <View
          style={{
            flexDirection: "row",
            marginTop: 4,
            width: "100%",
            justifyContent: "center",
          }}
        >
          <Input
            placeholder={Password}
            value={this.state.password}
            onChangeText={(text) => this.setPassword(text)}
            secureTextEntry={this.state.secureTextEntry}
          />
        </View>
        <Button onPress={() => this.login()}>
          <Text>SUBMIT</Text>
        </Button>
      </View>
    );
  }
}
