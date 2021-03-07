const BaseTool = cornerstoneTools.import("base/BaseTool");

class HelloWorldMouseTool extends BaseTool {
  constructor(configuration = {}) {
    super({
      name: configuration.name || "HelloWorldMouse",
      supportedInteractionTypes: ["Mouse"],
    });
  }

  preMouseDownCallback(evt) {
    console.log("Hello World");
  }
}