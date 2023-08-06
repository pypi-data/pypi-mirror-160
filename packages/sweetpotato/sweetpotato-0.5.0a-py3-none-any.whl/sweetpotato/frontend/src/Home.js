import React from "react";
import { Image } from "react-native";
import { Button, Layout, Text } from "@ui-kitten/components";

export class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <Layout
        style={{ justifyContent: "center", alignItems: "center", flex: 1 }}
      >
        <Image
          style={{ height: 200, width: 200, borderRadius: 50 }}
          source={{
            uri: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Ipomoea_batatas_006.JPG/1920px",
          }}
        />
        <Text style={{ margin: 25 }}>Sweet, Sweet Potatoes</Text>
        <Button onPress={() => alert("This app was made with sweetpotato")}>
          <Text>Info</Text>
        </Button>
      </Layout>
    );
  }
}
