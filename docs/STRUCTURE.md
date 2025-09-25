---
uid: goldilocks.structure
title: Project Structure
description: File organization, module descriptions, and dependency mapping for Goldilocks
author: Goldilocks Development Team
ms.date: 2025-09-25
---

This document explains the organized project structure and where to find different types of files.

> [!NOTE]
> This structure is automatically generated during documentation builds to ensure accuracy.

## Directory Structure

> [!NOTE]
> This structure is automatically generated during documentation builds to ensure accuracy.

```text
├── .benchmarks
│   ├── build_20250924_161237.json
│   ├── build_20250924_161314.json
│   ├── build_20250924_161402.json
│   ├── build_20250925_101238.json
│   ├── build_20250925_101332.json
│   ├── build_20250925_101626.json
│   ├── build_20250925_101949.json
│   ├── devcontainer-build-benchmark.sh
│   └── latest_benchmark_summary.txt
├── .devcontainer
│   ├── scripts
│   │   ├── generate-lock.sh
│   │   ├── performance-test.sh
│   │   └── post-create.sh
│   ├── devcontainer-lock.json
│   └── devcontainer.json
├── .github
│   ├── workflows
│   │   └── ci.yml
│   ├── copilot-instructions.md
│   └── dependabot.yml
├── .vscode
│   ├── launch.json
│   ├── settings.json
│   └── tasks.json
├── config
│   ├── .flake8
│   ├── .pre-commit-config.yaml
│   ├── cypress.config.js
│   ├── globals.xml
│   └── pyproject.toml
├── cypress
│   ├── e2e
│   │   └── smoke.cy.js
│   └── support
│       └── e2e.js
├── docs
│   ├── bin
│   │   ├── .playwright
│   │   │   └── package
│   │   │       ├── bin
│   │   │       │   ├── install_media_pack.ps1
│   │   │       │   ├── reinstall_chrome_beta_linux.sh
│   │   │       │   ├── reinstall_chrome_beta_mac.sh
│   │   │       │   ├── reinstall_chrome_beta_win.ps1
│   │   │       │   ├── reinstall_chrome_stable_linux.sh
│   │   │       │   ├── reinstall_chrome_stable_mac.sh
│   │   │       │   ├── reinstall_chrome_stable_win.ps1
│   │   │       │   ├── reinstall_msedge_beta_linux.sh
│   │   │       │   ├── reinstall_msedge_beta_mac.sh
│   │   │       │   ├── reinstall_msedge_beta_win.ps1
│   │   │       │   ├── reinstall_msedge_dev_linux.sh
│   │   │       │   ├── reinstall_msedge_dev_mac.sh
│   │   │       │   ├── reinstall_msedge_dev_win.ps1
│   │   │       │   ├── reinstall_msedge_stable_linux.sh
│   │   │       │   ├── reinstall_msedge_stable_mac.sh
│   │   │       │   └── reinstall_msedge_stable_win.ps1
│   │   │       ├── lib
│   │   │       │   ├── cli
│   │   │       │   │   ├── driver.js
│   │   │       │   │   ├── program.js
│   │   │       │   │   └── programWithTestStub.js
│   │   │       │   ├── client
│   │   │       │   │   ├── accessibility.js
│   │   │       │   │   ├── android.js
│   │   │       │   │   ├── api.js
│   │   │       │   │   ├── artifact.js
│   │   │       │   │   ├── browser.js
│   │   │       │   │   ├── browserContext.js
│   │   │       │   │   ├── browserType.js
│   │   │       │   │   ├── cdpSession.js
│   │   │       │   │   ├── channelOwner.js
│   │   │       │   │   ├── clientHelper.js
│   │   │       │   │   ├── clientInstrumentation.js
│   │   │       │   │   ├── clock.js
│   │   │       │   │   ├── connection.js
│   │   │       │   │   ├── consoleMessage.js
│   │   │       │   │   ├── coverage.js
│   │   │       │   │   ├── dialog.js
│   │   │       │   │   ├── download.js
│   │   │       │   │   ├── electron.js
│   │   │       │   │   ├── elementHandle.js
│   │   │       │   │   ├── errors.js
│   │   │       │   │   ├── eventEmitter.js
│   │   │       │   │   ├── events.js
│   │   │       │   │   ├── fetch.js
│   │   │       │   │   ├── fileChooser.js
│   │   │       │   │   ├── frame.js
│   │   │       │   │   ├── harRouter.js
│   │   │       │   │   ├── input.js
│   │   │       │   │   ├── jsHandle.js
│   │   │       │   │   ├── jsonPipe.js
│   │   │       │   │   ├── localUtils.js
│   │   │       │   │   ├── locator.js
│   │   │       │   │   ├── network.js
│   │   │       │   │   ├── page.js
│   │   │       │   │   ├── playwright.js
│   │   │       │   │   ├── selectors.js
│   │   │       │   │   ├── stream.js
│   │   │       │   │   ├── tracing.js
│   │   │       │   │   ├── types.js
│   │   │       │   │   ├── video.js
│   │   │       │   │   ├── waiter.js
│   │   │       │   │   ├── webError.js
│   │   │       │   │   ├── worker.js
│   │   │       │   │   └── writableStream.js
│   │   │       │   ├── common
│   │   │       │   │   ├── socksProxy.js
│   │   │       │   │   ├── timeoutSettings.js
│   │   │       │   │   └── types.js
│   │   │       │   ├── generated
│   │   │       │   │   ├── clockSource.js
│   │   │       │   │   ├── consoleApiSource.js
│   │   │       │   │   ├── injectedScriptSource.js
│   │   │       │   │   ├── pollingRecorderSource.js
│   │   │       │   │   ├── utilityScriptSource.js
│   │   │       │   │   └── webSocketMockSource.js
│   │   │       │   ├── image_tools
│   │   │       │   │   ├── colorUtils.js
│   │   │       │   │   ├── compare.js
│   │   │       │   │   ├── imageChannel.js
│   │   │       │   │   └── stats.js
│   │   │       │   ├── protocol
│   │   │       │   │   ├── debug.js
│   │   │       │   │   ├── serializers.js
│   │   │       │   │   ├── transport.js
│   │   │       │   │   ├── validator.js
│   │   │       │   │   └── validatorPrimitives.js
│   │   │       │   ├── remote
│   │   │       │   │   ├── playwrightConnection.js
│   │   │       │   │   └── playwrightServer.js
│   │   │       │   ├── server
│   │   │       │   │   ├── android
│   │   │       │   │   │   ├── android.js
│   │   │       │   │   │   └── backendAdb.js
│   │   │       │   │   ├── bidi
│   │   │       │   │   │   ├── third_party
│   │   │       │   │   │   │   ├── bidiDeserializer.js
│   │   │       │   │   │   │   ├── bidiKeyboard.js
│   │   │       │   │   │   │   ├── bidiProtocol.js
│   │   │       │   │   │   │   ├── bidiSerializer.js
│   │   │       │   │   │   │   └── firefoxPrefs.js
│   │   │       │   │   │   ├── bidiBrowser.js
│   │   │       │   │   │   ├── bidiChromium.js
│   │   │       │   │   │   ├── bidiConnection.js
│   │   │       │   │   │   ├── bidiExecutionContext.js
│   │   │       │   │   │   ├── bidiFirefox.js
│   │   │       │   │   │   ├── bidiInput.js
│   │   │       │   │   │   ├── bidiNetworkManager.js
│   │   │       │   │   │   ├── bidiOverCdp.js
│   │   │       │   │   │   ├── bidiPage.js
│   │   │       │   │   │   └── bidiPdf.js
│   │   │       │   │   ├── chromium
│   │   │       │   │   │   ├── appIcon.png
│   │   │       │   │   │   ├── chromium.js
│   │   │       │   │   │   ├── chromiumSwitches.js
│   │   │       │   │   │   ├── crAccessibility.js
│   │   │       │   │   │   ├── crBrowser.js
│   │   │       │   │   │   ├── crConnection.js
│   │   │       │   │   │   ├── crCoverage.js
│   │   │       │   │   │   ├── crDevTools.js
│   │   │       │   │   │   ├── crDragDrop.js
│   │   │       │   │   │   ├── crExecutionContext.js
│   │   │       │   │   │   ├── crInput.js
│   │   │       │   │   │   ├── crNetworkManager.js
│   │   │       │   │   │   ├── crPage.js
│   │   │       │   │   │   ├── crPdf.js
│   │   │       │   │   │   ├── crProtocolHelper.js
│   │   │       │   │   │   ├── crServiceWorker.js
│   │   │       │   │   │   ├── defaultFontFamilies.js
│   │   │       │   │   │   └── videoRecorder.js
│   │   │       │   │   ├── codegen
│   │   │       │   │   │   ├── csharp.js
│   │   │       │   │   │   ├── java.js
│   │   │       │   │   │   ├── javascript.js
│   │   │       │   │   │   ├── jsonl.js
│   │   │       │   │   │   ├── language.js
│   │   │       │   │   │   ├── languages.js
│   │   │       │   │   │   ├── python.js
│   │   │       │   │   │   └── types.js
│   │   │       │   │   ├── dispatchers
│   │   │       │   │   │   ├── androidDispatcher.js
│   │   │       │   │   │   ├── artifactDispatcher.js
│   │   │       │   │   │   ├── browserContextDispatcher.js
│   │   │       │   │   │   ├── browserDispatcher.js
│   │   │       │   │   │   ├── browserTypeDispatcher.js
│   │   │       │   │   │   ├── cdpSessionDispatcher.js
│   │   │       │   │   │   ├── debugControllerDispatcher.js
│   │   │       │   │   │   ├── dialogDispatcher.js
│   │   │       │   │   │   ├── dispatcher.js
│   │   │       │   │   │   ├── electronDispatcher.js
│   │   │       │   │   │   ├── elementHandlerDispatcher.js
│   │   │       │   │   │   ├── frameDispatcher.js
│   │   │       │   │   │   ├── jsHandleDispatcher.js
│   │   │       │   │   │   ├── jsonPipeDispatcher.js
│   │   │       │   │   │   ├── localUtilsDispatcher.js
│   │   │       │   │   │   ├── networkDispatchers.js
│   │   │       │   │   │   ├── pageDispatcher.js
│   │   │       │   │   │   ├── playwrightDispatcher.js
│   │   │       │   │   │   ├── selectorsDispatcher.js
│   │   │       │   │   │   ├── streamDispatcher.js
│   │   │       │   │   │   ├── tracingDispatcher.js
│   │   │       │   │   │   ├── webSocketRouteDispatcher.js
│   │   │       │   │   │   └── writableStreamDispatcher.js
│   │   │       │   │   ├── electron
│   │   │       │   │   │   ├── electron.js
│   │   │       │   │   │   └── loader.js
│   │   │       │   │   ├── firefox
│   │   │       │   │   │   ├── ffAccessibility.js
│   │   │       │   │   │   ├── ffBrowser.js
│   │   │       │   │   │   ├── ffConnection.js
│   │   │       │   │   │   ├── ffExecutionContext.js
│   │   │       │   │   │   ├── ffInput.js
│   │   │       │   │   │   ├── ffNetworkManager.js
│   │   │       │   │   │   ├── ffPage.js
│   │   │       │   │   │   └── firefox.js
│   │   │       │   │   ├── har
│   │   │       │   │   │   ├── harRecorder.js
│   │   │       │   │   │   └── harTracer.js
│   │   │       │   │   ├── isomorphic
│   │   │       │   │   │   └── utilityScriptSerializers.js
│   │   │       │   │   ├── recorder
│   │   │       │   │   │   ├── chat.js
│   │   │       │   │   │   ├── contextRecorder.js
│   │   │       │   │   │   ├── recorderApp.js
│   │   │       │   │   │   ├── recorderCollection.js
│   │   │       │   │   │   ├── recorderFrontend.js
│   │   │       │   │   │   ├── recorderRunner.js
│   │   │       │   │   │   ├── recorderUtils.js
│   │   │       │   │   │   └── throttledFile.js
│   │   │       │   │   ├── registry
│   │   │       │   │   │   ├── browserFetcher.js
│   │   │       │   │   │   ├── dependencies.js
│   │   │       │   │   │   ├── index.js
│   │   │       │   │   │   ├── nativeDeps.js
│   │   │       │   │   │   └── oopDownloadBrowserMain.js
│   │   │       │   │   ├── trace
│   │   │       │   │   │   ├── recorder
│   │   │       │   │   │   │   ├── snapshotter.js
│   │   │       │   │   │   │   ├── snapshotterInjected.js
│   │   │       │   │   │   │   └── tracing.js
│   │   │       │   │   │   ├── test
│   │   │       │   │   │   │   └── inMemorySnapshotter.js
│   │   │       │   │   │   └── viewer
│   │   │       │   │   │       └── traceViewer.js
│   │   │       │   │   ├── webkit
│   │   │       │   │   │   ├── webkit.js
│   │   │       │   │   │   ├── wkAccessibility.js
│   │   │       │   │   │   ├── wkBrowser.js
│   │   │       │   │   │   ├── wkConnection.js
│   │   │       │   │   │   ├── wkExecutionContext.js
│   │   │       │   │   │   ├── wkInput.js
│   │   │       │   │   │   ├── wkInterceptableRequest.js
│   │   │       │   │   │   ├── wkPage.js
│   │   │       │   │   │   ├── wkProvisionalPage.js
│   │   │       │   │   │   └── wkWorkers.js
│   │   │       │   │   ├── accessibility.js
│   │   │       │   │   ├── artifact.js
│   │   │       │   │   ├── browser.js
│   │   │       │   │   ├── browserContext.js
│   │   │       │   │   ├── browserType.js
│   │   │       │   │   ├── clock.js
│   │   │       │   │   ├── console.js
│   │   │       │   │   ├── cookieStore.js
│   │   │       │   │   ├── debugController.js
│   │   │       │   │   ├── debugger.js
│   │   │       │   │   ├── deviceDescriptors.js
│   │   │       │   │   ├── deviceDescriptorsSource.json
│   │   │       │   │   ├── dialog.js
│   │   │       │   │   ├── dom.js
│   │   │       │   │   ├── download.js
│   │   │       │   │   ├── errors.js
│   │   │       │   │   ├── fetch.js
│   │   │       │   │   ├── fileChooser.js
│   │   │       │   │   ├── fileUploadUtils.js
│   │   │       │   │   ├── formData.js
│   │   │       │   │   ├── frameSelectors.js
│   │   │       │   │   ├── frames.js
│   │   │       │   │   ├── helper.js
│   │   │       │   │   ├── index.js
│   │   │       │   │   ├── input.js
│   │   │       │   │   ├── instrumentation.js
│   │   │       │   │   ├── javascript.js
│   │   │       │   │   ├── launchApp.js
│   │   │       │   │   ├── macEditingCommands.js
│   │   │       │   │   ├── network.js
│   │   │       │   │   ├── page.js
│   │   │       │   │   ├── pipeTransport.js
│   │   │       │   │   ├── playwright.js
│   │   │       │   │   ├── progress.js
│   │   │       │   │   ├── protocolError.js
│   │   │       │   │   ├── recorder.js
│   │   │       │   │   ├── screenshotter.js
│   │   │       │   │   ├── selectors.js
│   │   │       │   │   ├── socksClientCertificatesInterceptor.js
│   │   │       │   │   ├── socksInterceptor.js
│   │   │       │   │   ├── transport.js
│   │   │       │   │   ├── types.js
│   │   │       │   │   └── usKeyboardLayout.js
│   │   │       │   ├── third_party
│   │   │       │   │   └── pixelmatch.js
│   │   │       │   ├── utils
│   │   │       │   │   ├── isomorphic
│   │   │       │   │   │   ├── ariaSnapshot.js
│   │   │       │   │   │   ├── cssParser.js
│   │   │       │   │   │   ├── cssTokenizer.js
│   │   │       │   │   │   ├── locatorGenerators.js
│   │   │       │   │   │   ├── locatorParser.js
│   │   │       │   │   │   ├── locatorUtils.js
│   │   │       │   │   │   ├── mimeType.js
│   │   │       │   │   │   ├── selectorParser.js
│   │   │       │   │   │   ├── stringUtils.js
│   │   │       │   │   │   ├── traceUtils.js
│   │   │       │   │   │   └── urlMatch.js
│   │   │       │   │   ├── ascii.js
│   │   │       │   │   ├── comparators.js
│   │   │       │   │   ├── crypto.js
│   │   │       │   │   ├── debug.js
│   │   │       │   │   ├── debugLogger.js
│   │   │       │   │   ├── env.js
│   │   │       │   │   ├── eventsHelper.js
│   │   │       │   │   ├── expectUtils.js
│   │   │       │   │   ├── fileUtils.js
│   │   │       │   │   ├── happy-eyeballs.js
│   │   │       │   │   ├── headers.js
│   │   │       │   │   ├── hostPlatform.js
│   │   │       │   │   ├── httpServer.js
│   │   │       │   │   ├── index.js
│   │   │       │   │   ├── linuxUtils.js
│   │   │       │   │   ├── manualPromise.js
│   │   │       │   │   ├── multimap.js
│   │   │       │   │   ├── network.js
│   │   │       │   │   ├── processLauncher.js
│   │   │       │   │   ├── profiler.js
│   │   │       │   │   ├── rtti.js
│   │   │       │   │   ├── semaphore.js
│   │   │       │   │   ├── sequence.js
│   │   │       │   │   ├── spawnAsync.js
│   │   │       │   │   ├── stackTrace.js
│   │   │       │   │   ├── task.js
│   │   │       │   │   ├── time.js
│   │   │       │   │   ├── timeoutRunner.js
│   │   │       │   │   ├── traceUtils.js
│   │   │       │   │   ├── userAgent.js
│   │   │       │   │   ├── wsServer.js
│   │   │       │   │   ├── zipFile.js
│   │   │       │   │   └── zones.js
│   │   │       │   ├── utilsBundleImpl
│   │   │       │   │   ├── index.js
│   │   │       │   │   └── xdg-open
│   │   │       │   ├── vite
│   │   │       │   │   ├── htmlReport
│   │   │       │   │   │   └── index.html
│   │   │       │   │   ├── recorder
│   │   │       │   │   │   ├── assets
│   │   │       │   │   │   │   ├── codeMirrorModule-C3UTv-Ge.css
│   │   │       │   │   │   │   ├── codeMirrorModule-k-61wZCK.js
│   │   │       │   │   │   │   ├── codicon-DCmgc-ay.ttf
│   │   │       │   │   │   │   ├── index-B70BEW3b.js
│   │   │       │   │   │   │   └── index-eHBmevrY.css
│   │   │       │   │   │   ├── index.html
│   │   │       │   │   │   └── playwright-logo.svg
│   │   │       │   │   └── traceViewer
│   │   │       │   │       ├── assets
│   │   │       │   │       │   ├── codeMirrorModule-CyuxU5C-.js
│   │   │       │   │       │   ├── defaultSettingsView-5nVJRt0A.js
│   │   │       │   │       │   └── xtermModule-c-SNdYZy.js
│   │   │       │   │       ├── codeMirrorModule.C3UTv-Ge.css
│   │   │       │   │       ├── codicon.DCmgc-ay.ttf
│   │   │       │   │       ├── defaultSettingsView.2xeEXCXv.css
│   │   │       │   │       ├── index.CFOW-Ezb.css
│   │   │       │   │       ├── index.html
│   │   │       │   │       ├── index.qVn2ZnpC.js
│   │   │       │   │       ├── playwright-logo.svg
│   │   │       │   │       ├── snapshot.html
│   │   │       │   │       ├── sw.bundle.js
│   │   │       │   │       ├── uiMode.BatfzHMG.css
│   │   │       │   │       ├── uiMode.html
│   │   │       │   │       ├── uiMode.m4IPRPOd.js
│   │   │       │   │       └── xtermModule.Beg8tuEN.css
│   │   │       │   ├── androidServerImpl.js
│   │   │       │   ├── browserServerImpl.js
│   │   │       │   ├── inProcessFactory.js
│   │   │       │   ├── inprocess.js
│   │   │       │   ├── outofprocess.js
│   │   │       │   ├── utilsBundle.js
│   │   │       │   ├── zipBundle.js
│   │   │       │   └── zipBundleImpl.js
│   │   │       ├── types
│   │   │       │   ├── protocol.d.ts
│   │   │       │   ├── structs.d.ts
│   │   │       │   └── types.d.ts
│   │   │       ├── README.md
│   │   │       ├── ThirdPartyNotices.txt
│   │   │       ├── api.json
│   │   │       ├── browsers.json
│   │   │       ├── cli.js
│   │   │       ├── index.d.ts
│   │   │       ├── index.js
│   │   │       ├── index.mjs
│   │   │       ├── package.json
│   │   │       └── protocol.yml
│   │   ├── BuildHost-net472
│   │   │   ├── cs
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── de
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── es
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── fr
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── it
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── ja
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── ko
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── pl
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── pt-BR
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── ru
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── tr
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── zh-Hans
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── zh-Hant
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── Microsoft.Bcl.AsyncInterfaces.dll
│   │   │   ├── Microsoft.Build.Locator.dll
│   │   │   ├── Microsoft.CodeAnalysis.Workspaces.MSBuild.BuildHost.exe
│   │   │   ├── Microsoft.CodeAnalysis.Workspaces.MSBuild.BuildHost.exe.config
│   │   │   ├── Microsoft.IO.Redist.dll
│   │   │   ├── Newtonsoft.Json.dll
│   │   │   ├── System.Buffers.dll
│   │   │   ├── System.Collections.Immutable.dll
│   │   │   ├── System.CommandLine.dll
│   │   │   ├── System.Memory.dll
│   │   │   ├── System.Numerics.Vectors.dll
│   │   │   ├── System.Runtime.CompilerServices.Unsafe.dll
│   │   │   ├── System.Text.Encodings.Web.dll
│   │   │   ├── System.Text.Json.dll
│   │   │   ├── System.Threading.Tasks.Extensions.dll
│   │   │   └── System.ValueTuple.dll
│   │   ├── BuildHost-netcore
│   │   │   ├── cs
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── de
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── es
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── fr
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── it
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── ja
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── ko
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── pl
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── pt-BR
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── ru
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── runtimes
│   │   │   │   └── browser
│   │   │   │       └── lib
│   │   │   │           └── net6.0
│   │   │   │               └── System.Text.Encodings.Web.dll
│   │   │   ├── tr
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── zh-Hans
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── zh-Hant
│   │   │   │   └── System.CommandLine.resources.dll
│   │   │   ├── Microsoft.Build.Locator.dll
│   │   │   ├── Microsoft.CodeAnalysis.Workspaces.MSBuild.BuildHost.deps.json
│   │   │   ├── Microsoft.CodeAnalysis.Workspaces.MSBuild.BuildHost.dll
│   │   │   ├── Microsoft.CodeAnalysis.Workspaces.MSBuild.BuildHost.dll.config
│   │   │   ├── Microsoft.CodeAnalysis.Workspaces.MSBuild.BuildHost.runtimeconfig.json
│   │   │   ├── Newtonsoft.Json.dll
│   │   │   ├── System.Collections.Immutable.dll
│   │   │   ├── System.CommandLine.dll
│   │   │   ├── System.Text.Encodings.Web.dll
│   │   │   └── System.Text.Json.dll
│   │   ├── templates
│   │   │   ├── common
│   │   │   │   ├── partials
│   │   │   │   │   ├── classSubtitle.tmpl.partial
│   │   │   │   │   └── namespaceSubtitle.tmpl.partial
│   │   │   │   ├── ManagedReference.common.js
│   │   │   │   ├── RestApi.common.js
│   │   │   │   ├── UniversalReference.common.js
│   │   │   │   └── common.js
│   │   │   ├── default
│   │   │   │   ├── layout
│   │   │   │   │   └── _master.tmpl
│   │   │   │   ├── partials
│   │   │   │   │   ├── uref
│   │   │   │   │   │   ├── class.header.tmpl.partial
│   │   │   │   │   │   ├── class.tmpl.partial
│   │   │   │   │   │   ├── enum.tmpl.partial
│   │   │   │   │   │   ├── inheritance.tmpl.partial
│   │   │   │   │   │   ├── namespace.tmpl.partial
│   │   │   │   │   │   └── parameters.tmpl.partial
│   │   │   │   │   ├── affix.tmpl.partial
│   │   │   │   │   ├── breadcrumb.tmpl.partial
│   │   │   │   │   ├── class.header.tmpl.partial
│   │   │   │   │   ├── class.memberpage.tmpl.partial
│   │   │   │   │   ├── class.tmpl.partial
│   │   │   │   │   ├── classSubtitle.tmpl.partial
│   │   │   │   │   ├── collection.tmpl.partial
│   │   │   │   │   ├── customMREFContent.tmpl.partial
│   │   │   │   │   ├── dd-li.tmpl.partial
│   │   │   │   │   ├── enum.tmpl.partial
│   │   │   │   │   ├── footer.tmpl.partial
│   │   │   │   │   ├── head.tmpl.partial
│   │   │   │   │   ├── item.tmpl.partial
│   │   │   │   │   ├── li.tmpl.partial
│   │   │   │   │   ├── logo.tmpl.partial
│   │   │   │   │   ├── namespace.tmpl.partial
│   │   │   │   │   ├── namespaceSubtitle.tmpl.partial
│   │   │   │   │   ├── navbar.tmpl.partial
│   │   │   │   │   ├── rest.child.tmpl.partial
│   │   │   │   │   ├── rest.definition.tmpl.partial
│   │   │   │   │   ├── rest.tmpl.partial
│   │   │   │   │   ├── scripts.tmpl.partial
│   │   │   │   │   ├── searchResults.tmpl.partial
│   │   │   │   │   ├── title.tmpl.partial
│   │   │   │   │   └── toc.tmpl.partial
│   │   │   │   ├── styles
│   │   │   │   │   ├── docfx.css
│   │   │   │   │   ├── docfx.js
│   │   │   │   │   ├── docfx.vendor.min.css
│   │   │   │   │   ├── docfx.vendor.min.css.map
│   │   │   │   │   ├── docfx.vendor.min.js
│   │   │   │   │   ├── docfx.vendor.min.js.map
│   │   │   │   │   ├── glyphicons-halflings-regular-ACNUA6UY.ttf
│   │   │   │   │   ├── glyphicons-halflings-regular-JOUF32XT.woff
│   │   │   │   │   ├── glyphicons-halflings-regular-PIHUWCJO.eot
│   │   │   │   │   ├── glyphicons-halflings-regular-QXYEM3FU.svg
│   │   │   │   │   ├── glyphicons-halflings-regular-W4DYDFZM.woff2
│   │   │   │   │   ├── main.css
│   │   │   │   │   ├── main.js
│   │   │   │   │   ├── search-worker.min.js
│   │   │   │   │   └── search-worker.min.js.map
│   │   │   │   ├── ManagedReference.common.js
│   │   │   │   ├── ManagedReference.extension.js
│   │   │   │   ├── ManagedReference.html.primary.js
│   │   │   │   ├── ManagedReference.html.primary.tmpl
│   │   │   │   ├── Redirection.html.primary.tmpl
│   │   │   │   ├── RestApi.common.js
│   │   │   │   ├── RestApi.extension.js
│   │   │   │   ├── RestApi.html.primary.js
│   │   │   │   ├── RestApi.html.primary.tmpl
│   │   │   │   ├── UniversalReference.common.js
│   │   │   │   ├── UniversalReference.extension.js
│   │   │   │   ├── UniversalReference.html.primary.js
│   │   │   │   ├── UniversalReference.html.primary.tmpl
│   │   │   │   ├── common.js
│   │   │   │   ├── conceptual.extension.js
│   │   │   │   ├── conceptual.html.primary.js
│   │   │   │   ├── conceptual.html.primary.tmpl
│   │   │   │   ├── favicon.ico
│   │   │   │   ├── logo.svg
│   │   │   │   ├── search-stopwords.json
│   │   │   │   ├── toc.extension.js
│   │   │   │   ├── toc.html.primary.js
│   │   │   │   ├── toc.html.primary.tmpl
│   │   │   │   ├── toc.json.js
│   │   │   │   ├── toc.json.tmpl
│   │   │   │   └── token.json
│   │   │   ├── default(zh-cn)
│   │   │   │   ├── partials
│   │   │   │   │   └── title.tmpl.partial
│   │   │   │   └── token.json
│   │   │   ├── modern
│   │   │   │   ├── layout
│   │   │   │   │   └── _master.tmpl
│   │   │   │   ├── partials
│   │   │   │   │   ├── class.header.tmpl.partial
│   │   │   │   │   ├── class.memberpage.tmpl.partial
│   │   │   │   │   ├── class.tmpl.partial
│   │   │   │   │   ├── collection.tmpl.partial
│   │   │   │   │   ├── customMREFContent.tmpl.partial
│   │   │   │   │   ├── enum.tmpl.partial
│   │   │   │   │   ├── item.tmpl.partial
│   │   │   │   │   └── namespace.tmpl.partial
│   │   │   │   ├── public
│   │   │   │   │   ├── architecture-I3QFYML2-2T2ZUHXO.min.js
│   │   │   │   │   ├── architecture-I3QFYML2-2T2ZUHXO.min.js.map
│   │   │   │   │   ├── architectureDiagram-UYN6MBPD-WBU2OYNU.min.js
│   │   │   │   │   ├── architectureDiagram-UYN6MBPD-WBU2OYNU.min.js.map
│   │   │   │   │   ├── blockDiagram-ZHA2E4KO-IZKTV5IP.min.js
│   │   │   │   │   ├── blockDiagram-ZHA2E4KO-IZKTV5IP.min.js.map
│   │   │   │   │   ├── bootstrap-icons-OCU552PF.woff
│   │   │   │   │   ├── bootstrap-icons-X6UQXWUS.woff2
│   │   │   │   │   ├── c4Diagram-6F5ED5ID-X53KYE5F.min.js
│   │   │   │   │   ├── c4Diagram-6F5ED5ID-X53KYE5F.min.js.map
│   │   │   │   │   ├── chunk-2YMHYP32.min.js
│   │   │   │   │   ├── chunk-2YMHYP32.min.js.map
│   │   │   │   │   ├── chunk-33FU46FA.min.js
│   │   │   │   │   ├── chunk-33FU46FA.min.js.map
│   │   │   │   │   ├── chunk-3Z74ZUXG.min.js
│   │   │   │   │   ├── chunk-3Z74ZUXG.min.js.map
│   │   │   │   │   ├── chunk-54U54PUP.min.js
│   │   │   │   │   ├── chunk-54U54PUP.min.js.map
│   │   │   │   │   ├── chunk-5IIW54K6.min.js
│   │   │   │   │   ├── chunk-5IIW54K6.min.js.map
│   │   │   │   │   ├── chunk-6YMKSKZH.min.js
│   │   │   │   │   ├── chunk-6YMKSKZH.min.js.map
│   │   │   │   │   ├── chunk-AUO2PXKS.min.js
│   │   │   │   │   ├── chunk-AUO2PXKS.min.js.map
│   │   │   │   │   ├── chunk-BD4P4Z7J.min.js
│   │   │   │   │   ├── chunk-BD4P4Z7J.min.js.map
│   │   │   │   │   ├── chunk-BIJFJY5F.min.js
│   │   │   │   │   ├── chunk-BIJFJY5F.min.js.map
│   │   │   │   │   ├── chunk-C7DS3QYJ.min.js
│   │   │   │   │   ├── chunk-C7DS3QYJ.min.js.map
│   │   │   │   │   ├── chunk-CLIYZZ5Y.min.js
│   │   │   │   │   ├── chunk-CLIYZZ5Y.min.js.map
│   │   │   │   │   ├── chunk-CM5D5KZN.min.js
│   │   │   │   │   ├── chunk-CM5D5KZN.min.js.map
│   │   │   │   │   ├── chunk-CXRPJJJE.min.js
│   │   │   │   │   ├── chunk-CXRPJJJE.min.js.map
│   │   │   │   │   ├── chunk-DTUU2GN4.min.js
│   │   │   │   │   ├── chunk-DTUU2GN4.min.js.map
│   │   │   │   │   ├── chunk-EDJWACL4.min.js
│   │   │   │   │   ├── chunk-EDJWACL4.min.js.map
│   │   │   │   │   ├── chunk-EKP7MBOP.min.js
│   │   │   │   │   ├── chunk-EKP7MBOP.min.js.map
│   │   │   │   │   ├── chunk-I4ZXTPQC.min.js
│   │   │   │   │   ├── chunk-I4ZXTPQC.min.js.map
│   │   │   │   │   ├── chunk-IJ4BRSPX.min.js
│   │   │   │   │   ├── chunk-IJ4BRSPX.min.js.map
│   │   │   │   │   ├── chunk-IQQ46AC6.min.js
│   │   │   │   │   ├── chunk-IQQ46AC6.min.js.map
│   │   │   │   │   ├── chunk-ISDTAGDN.min.js
│   │   │   │   │   ├── chunk-ISDTAGDN.min.js.map
│   │   │   │   │   ├── chunk-JL3VILNY.min.js
│   │   │   │   │   ├── chunk-JL3VILNY.min.js.map
│   │   │   │   │   ├── chunk-N4YULA37.min.js
│   │   │   │   │   ├── chunk-N4YULA37.min.js.map
│   │   │   │   │   ├── chunk-N6ME3NZU.min.js
│   │   │   │   │   ├── chunk-N6ME3NZU.min.js.map
│   │   │   │   │   ├── chunk-OSRY5VT3.min.js
│   │   │   │   │   ├── chunk-OSRY5VT3.min.js.map
│   │   │   │   │   ├── chunk-OZ2RCKQJ.min.js
│   │   │   │   │   ├── chunk-OZ2RCKQJ.min.js.map
│   │   │   │   │   ├── chunk-PDS7545E.min.js
│   │   │   │   │   ├── chunk-PDS7545E.min.js.map
│   │   │   │   │   ├── chunk-PYPO7LRM.min.js
│   │   │   │   │   ├── chunk-PYPO7LRM.min.js.map
│   │   │   │   │   ├── chunk-TLYS76Q7.min.js
│   │   │   │   │   ├── chunk-TLYS76Q7.min.js.map
│   │   │   │   │   ├── chunk-U3SD26FK.min.js
│   │   │   │   │   ├── chunk-U3SD26FK.min.js.map
│   │   │   │   │   ├── chunk-U4DUTLYF.min.js
│   │   │   │   │   ├── chunk-U4DUTLYF.min.js.map
│   │   │   │   │   ├── chunk-UEFJDIUO.min.js
│   │   │   │   │   ├── chunk-UEFJDIUO.min.js.map
│   │   │   │   │   ├── chunk-V55NTXQN.min.js
│   │   │   │   │   ├── chunk-V55NTXQN.min.js.map
│   │   │   │   │   ├── chunk-WMZJ2DJX.min.js
│   │   │   │   │   ├── chunk-WMZJ2DJX.min.js.map
│   │   │   │   │   ├── chunk-WXIN66R4.min.js
│   │   │   │   │   ├── chunk-WXIN66R4.min.js.map
│   │   │   │   │   ├── classDiagram-LNE6IOMH-VZ67B4ZP.min.js
│   │   │   │   │   ├── classDiagram-LNE6IOMH-VZ67B4ZP.min.js.map
│   │   │   │   │   ├── classDiagram-v2-MQ7JQ4JX-4JTAVB6L.min.js
│   │   │   │   │   ├── classDiagram-v2-MQ7JQ4JX-4JTAVB6L.min.js.map
│   │   │   │   │   ├── dagre-4EVJKHTY-MHPLGZHX.min.js
│   │   │   │   │   ├── dagre-4EVJKHTY-MHPLGZHX.min.js.map
│   │   │   │   │   ├── diagram-QW4FP2JN-UOF7FAFC.min.js
│   │   │   │   │   ├── diagram-QW4FP2JN-UOF7FAFC.min.js.map
│   │   │   │   │   ├── docfx.min.css
│   │   │   │   │   ├── docfx.min.css.map
│   │   │   │   │   ├── docfx.min.js
│   │   │   │   │   ├── docfx.min.js.map
│   │   │   │   │   ├── erDiagram-6RL3IURR-PEYW6AVI.min.js
│   │   │   │   │   ├── erDiagram-6RL3IURR-PEYW6AVI.min.js.map
│   │   │   │   │   ├── es-4I4X6RME.min.js
│   │   │   │   │   ├── es-4I4X6RME.min.js.map
│   │   │   │   │   ├── flowDiagram-7ASYPVHJ-DABBKNEC.min.js
│   │   │   │   │   ├── flowDiagram-7ASYPVHJ-DABBKNEC.min.js.map
│   │   │   │   │   ├── ganttDiagram-NTVNEXSI-JVQ2N4MZ.min.js
│   │   │   │   │   ├── ganttDiagram-NTVNEXSI-JVQ2N4MZ.min.js.map
│   │   │   │   │   ├── gitGraph-YCYPL57B-3XOJ53I6.min.js
│   │   │   │   │   ├── gitGraph-YCYPL57B-3XOJ53I6.min.js.map
│   │   │   │   │   ├── gitGraphDiagram-NRZ2UAAF-WVTRWY3E.min.js
│   │   │   │   │   ├── gitGraphDiagram-NRZ2UAAF-WVTRWY3E.min.js.map
│   │   │   │   │   ├── info-46DW6VJ7-RDUIJSMX.min.js
│   │   │   │   │   ├── info-46DW6VJ7-RDUIJSMX.min.js.map
│   │   │   │   │   ├── infoDiagram-A4XQUW5V-SKLVFWJI.min.js
│   │   │   │   │   ├── infoDiagram-A4XQUW5V-SKLVFWJI.min.js.map
│   │   │   │   │   ├── journeyDiagram-G5WM74LC-AHZ7GKR5.min.js
│   │   │   │   │   ├── journeyDiagram-G5WM74LC-AHZ7GKR5.min.js.map
│   │   │   │   │   ├── kanban-definition-QRCXZQQD-MKSHYOCX.min.js
│   │   │   │   │   ├── kanban-definition-QRCXZQQD-MKSHYOCX.min.js.map
│   │   │   │   │   ├── katex-ROPKEHCO.min.js
│   │   │   │   │   ├── katex-ROPKEHCO.min.js.map
│   │   │   │   │   ├── lunr.ar-A6ZT2INA.min.js
│   │   │   │   │   ├── lunr.ar-A6ZT2INA.min.js.map
│   │   │   │   │   ├── lunr.da-WWM276CR.min.js
│   │   │   │   │   ├── lunr.da-WWM276CR.min.js.map
│   │   │   │   │   ├── lunr.de-XXPRKDAY.min.js
│   │   │   │   │   ├── lunr.de-XXPRKDAY.min.js.map
│   │   │   │   │   ├── lunr.du-NO4L2LL3.min.js
│   │   │   │   │   ├── lunr.du-NO4L2LL3.min.js.map
│   │   │   │   │   ├── lunr.el-5ZSSJVMA.min.js
│   │   │   │   │   ├── lunr.el-5ZSSJVMA.min.js.map
│   │   │   │   │   ├── lunr.es-ZH6Q76E6.min.js
│   │   │   │   │   ├── lunr.es-ZH6Q76E6.min.js.map
│   │   │   │   │   ├── lunr.fi-S7WJSBCP.min.js
│   │   │   │   │   ├── lunr.fi-S7WJSBCP.min.js.map
│   │   │   │   │   ├── lunr.fr-H2QNBELV.min.js
│   │   │   │   │   ├── lunr.fr-H2QNBELV.min.js.map
│   │   │   │   │   ├── lunr.he-TTLAK4MN.min.js
│   │   │   │   │   ├── lunr.he-TTLAK4MN.min.js.map
│   │   │   │   │   ├── lunr.hi-PWWMAGLU.min.js
│   │   │   │   │   ├── lunr.hi-PWWMAGLU.min.js.map
│   │   │   │   │   ├── lunr.hu-DLG2DSVM.min.js
│   │   │   │   │   ├── lunr.hu-DLG2DSVM.min.js.map
│   │   │   │   │   ├── lunr.hy-FFQJAR7M.min.js
│   │   │   │   │   ├── lunr.hy-FFQJAR7M.min.js.map
│   │   │   │   │   ├── lunr.it-VQNLJLPR.min.js
│   │   │   │   │   ├── lunr.it-VQNLJLPR.min.js.map
│   │   │   │   │   ├── lunr.ja-J6QHZSR2.min.js
│   │   │   │   │   ├── lunr.ja-J6QHZSR2.min.js.map
│   │   │   │   │   ├── lunr.jp-M45D3XJE.min.js
│   │   │   │   │   ├── lunr.jp-M45D3XJE.min.js.map
│   │   │   │   │   ├── lunr.kn-ASLXFRTC.min.js
│   │   │   │   │   ├── lunr.kn-ASLXFRTC.min.js.map
│   │   │   │   │   ├── lunr.ko-RHF2BDE4.min.js
│   │   │   │   │   ├── lunr.ko-RHF2BDE4.min.js.map
│   │   │   │   │   ├── lunr.nl-2BITG354.min.js
│   │   │   │   │   ├── lunr.nl-2BITG354.min.js.map
│   │   │   │   │   ├── lunr.no-WPLSHWFO.min.js
│   │   │   │   │   ├── lunr.no-WPLSHWFO.min.js.map
│   │   │   │   │   ├── lunr.pt-V2XEBELC.min.js
│   │   │   │   │   ├── lunr.pt-V2XEBELC.min.js.map
│   │   │   │   │   ├── lunr.ro-O76266FJ.min.js
│   │   │   │   │   ├── lunr.ro-O76266FJ.min.js.map
│   │   │   │   │   ├── lunr.ru-G56UDXYH.min.js
│   │   │   │   │   ├── lunr.ru-G56UDXYH.min.js.map
│   │   │   │   │   ├── lunr.sa-LD5PRAIS.min.js
│   │   │   │   │   ├── lunr.sa-LD5PRAIS.min.js.map
│   │   │   │   │   ├── lunr.sv-7VRY4UDB.min.js
│   │   │   │   │   ├── lunr.sv-7VRY4UDB.min.js.map
│   │   │   │   │   ├── lunr.ta-OWB7AURB.min.js
│   │   │   │   │   ├── lunr.ta-OWB7AURB.min.js.map
│   │   │   │   │   ├── lunr.te-JGGL3BFP.min.js
│   │   │   │   │   ├── lunr.te-JGGL3BFP.min.js.map
│   │   │   │   │   ├── lunr.th-O4JBL3IY.min.js
│   │   │   │   │   ├── lunr.th-O4JBL3IY.min.js.map
│   │   │   │   │   ├── lunr.tr-WXUV733C.min.js
│   │   │   │   │   ├── lunr.tr-WXUV733C.min.js.map
│   │   │   │   │   ├── lunr.vi-3U4A337N.min.js
│   │   │   │   │   ├── lunr.vi-3U4A337N.min.js.map
│   │   │   │   │   ├── main.css
│   │   │   │   │   ├── main.js
│   │   │   │   │   ├── mermaid.core-QWHI4VJR.min.js
│   │   │   │   │   ├── mermaid.core-QWHI4VJR.min.js.map
│   │   │   │   │   ├── mindmap-definition-GWI6TPTV-XCX7U2FR.min.js
│   │   │   │   │   ├── mindmap-definition-GWI6TPTV-XCX7U2FR.min.js.map
│   │   │   │   │   ├── packet-W2GHVCYJ-ZZMTAWKW.min.js
│   │   │   │   │   ├── packet-W2GHVCYJ-ZZMTAWKW.min.js.map
│   │   │   │   │   ├── pie-BEWT4RHE-VFWRUT6J.min.js
│   │   │   │   │   ├── pie-BEWT4RHE-VFWRUT6J.min.js.map
│   │   │   │   │   ├── pieDiagram-YF2LJOPJ-ITGVNBO2.min.js
│   │   │   │   │   ├── pieDiagram-YF2LJOPJ-ITGVNBO2.min.js.map
│   │   │   │   │   ├── quadrantDiagram-OS5C2QUG-BN35C5UH.min.js
│   │   │   │   │   ├── quadrantDiagram-OS5C2QUG-BN35C5UH.min.js.map
│   │   │   │   │   ├── requirementDiagram-MIRIMTAZ-CXICLXCG.min.js
│   │   │   │   │   ├── requirementDiagram-MIRIMTAZ-CXICLXCG.min.js.map
│   │   │   │   │   ├── sankeyDiagram-Y46BX6SQ-LTJNBPUP.min.js
│   │   │   │   │   ├── sankeyDiagram-Y46BX6SQ-LTJNBPUP.min.js.map
│   │   │   │   │   ├── search-worker.min.js
│   │   │   │   │   ├── search-worker.min.js.map
│   │   │   │   │   ├── sequenceDiagram-G6AWOVSC-UJVWCU2P.min.js
│   │   │   │   │   ├── sequenceDiagram-G6AWOVSC-UJVWCU2P.min.js.map
│   │   │   │   │   ├── stateDiagram-MAYHULR4-UPNPJ5ZA.min.js
│   │   │   │   │   ├── stateDiagram-MAYHULR4-UPNPJ5ZA.min.js.map
│   │   │   │   │   ├── stateDiagram-v2-4JROLMXI-COTI64PW.min.js
│   │   │   │   │   ├── stateDiagram-v2-4JROLMXI-COTI64PW.min.js.map
│   │   │   │   │   ├── tex-svg-full-SL33OL2J.min.js
│   │   │   │   │   ├── tex-svg-full-SL33OL2J.min.js.map
│   │   │   │   │   ├── timeline-definition-U7ZMHBDA-I7GF7M6N.min.js
│   │   │   │   │   ├── timeline-definition-U7ZMHBDA-I7GF7M6N.min.js.map
│   │   │   │   │   ├── xychartDiagram-6QU3TZC5-MQVPM64I.min.js
│   │   │   │   │   └── xychartDiagram-6QU3TZC5-MQVPM64I.min.js.map
│   │   │   │   ├── ApiPage.html.primary.js
│   │   │   │   └── ApiPage.html.primary.tmpl
│   │   │   └── statictoc
│   │   │       ├── layout
│   │   │       │   └── _master.tmpl
│   │   │       ├── partials
│   │   │       │   ├── uref
│   │   │       │   │   ├── class.header.tmpl.partial
│   │   │       │   │   ├── class.tmpl.partial
│   │   │       │   │   ├── enum.tmpl.partial
│   │   │       │   │   ├── inheritance.tmpl.partial
│   │   │       │   │   ├── namespace.tmpl.partial
│   │   │       │   │   └── parameters.tmpl.partial
│   │   │       │   ├── affix.tmpl.partial
│   │   │       │   ├── breadcrumb.tmpl.partial
│   │   │       │   ├── class.header.tmpl.partial
│   │   │       │   ├── class.memberpage.tmpl.partial
│   │   │       │   ├── class.tmpl.partial
│   │   │       │   ├── classSubtitle.tmpl.partial
│   │   │       │   ├── collection.tmpl.partial
│   │   │       │   ├── customMREFContent.tmpl.partial
│   │   │       │   ├── dd-li.tmpl.partial
│   │   │       │   ├── enum.tmpl.partial
│   │   │       │   ├── footer.tmpl.partial
│   │   │       │   ├── head.tmpl.partial
│   │   │       │   ├── item.tmpl.partial
│   │   │       │   ├── li.tmpl.partial
│   │   │       │   ├── logo.tmpl.partial
│   │   │       │   ├── namespace.tmpl.partial
│   │   │       │   ├── namespaceSubtitle.tmpl.partial
│   │   │       │   ├── navbar-li.tmpl.partial
│   │   │       │   ├── navbar.tmpl.partial
│   │   │       │   ├── rest.child.tmpl.partial
│   │   │       │   ├── rest.definition.tmpl.partial
│   │   │       │   ├── rest.tmpl.partial
│   │   │       │   ├── scripts.tmpl.partial
│   │   │       │   ├── searchResults.tmpl.partial
│   │   │       │   ├── title.tmpl.partial
│   │   │       │   └── toc.tmpl.partial
│   │   │       ├── styles
│   │   │       │   ├── docfx.css
│   │   │       │   ├── docfx.js
│   │   │       │   ├── docfx.vendor.min.css
│   │   │       │   ├── docfx.vendor.min.css.map
│   │   │       │   ├── docfx.vendor.min.js
│   │   │       │   ├── docfx.vendor.min.js.map
│   │   │       │   ├── glyphicons-halflings-regular-ACNUA6UY.ttf
│   │   │       │   ├── glyphicons-halflings-regular-JOUF32XT.woff
│   │   │       │   ├── glyphicons-halflings-regular-PIHUWCJO.eot
│   │   │       │   ├── glyphicons-halflings-regular-QXYEM3FU.svg
│   │   │       │   ├── glyphicons-halflings-regular-W4DYDFZM.woff2
│   │   │       │   ├── main.css
│   │   │       │   ├── main.js
│   │   │       │   ├── search-worker.min.js
│   │   │       │   └── search-worker.min.js.map
│   │   │       ├── ManagedReference.common.js
│   │   │       ├── ManagedReference.extension.js
│   │   │       ├── ManagedReference.html.primary.js
│   │   │       ├── ManagedReference.html.primary.tmpl
│   │   │       ├── Redirection.html.primary.tmpl
│   │   │       ├── RestApi.common.js
│   │   │       ├── RestApi.extension.js
│   │   │       ├── RestApi.html.primary.js
│   │   │       ├── RestApi.html.primary.tmpl
│   │   │       ├── UniversalReference.common.js
│   │   │       ├── UniversalReference.extension.js
│   │   │       ├── UniversalReference.html.primary.js
│   │   │       ├── UniversalReference.html.primary.tmpl
│   │   │       ├── common.js
│   │   │       ├── conceptual.extension.js
│   │   │       ├── conceptual.html.primary.js
│   │   │       ├── conceptual.html.primary.tmpl
│   │   │       ├── favicon.ico
│   │   │       ├── logo.svg
│   │   │       ├── search-stopwords.json
│   │   │       ├── statictoc.util.js
│   │   │       ├── toc.extension.js
│   │   │       ├── toc.json.js
│   │   │       ├── toc.json.tmpl
│   │   │       ├── toc.tmpl.js
│   │   │       └── token.json
│   │   ├── .copilotignore
│   │   ├── .gitignore
│   │   ├── Acornima.dll
│   │   ├── Docfx.App.dll
│   │   ├── Docfx.App.pdb
│   │   ├── Docfx.Build.Common.dll
│   │   ├── Docfx.Build.Common.pdb
│   │   ├── Docfx.Build.ManagedReference.dll
│   │   ├── Docfx.Build.ManagedReference.pdb
│   │   ├── Docfx.Build.OverwriteDocuments.dll
│   │   ├── Docfx.Build.OverwriteDocuments.pdb
│   │   ├── Docfx.Build.RestApi.dll
│   │   ├── Docfx.Build.RestApi.pdb
│   │   ├── Docfx.Build.SchemaDriven.dll
│   │   ├── Docfx.Build.SchemaDriven.pdb
│   │   ├── Docfx.Build.UniversalReference.dll
│   │   ├── Docfx.Build.UniversalReference.pdb
│   │   ├── Docfx.Build.dll
│   │   ├── Docfx.Build.pdb
│   │   ├── Docfx.Common.dll
│   │   ├── Docfx.Common.pdb
│   │   ├── Docfx.DataContracts.Common.dll
│   │   ├── Docfx.DataContracts.Common.pdb
│   │   ├── Docfx.DataContracts.RestApi.dll
│   │   ├── Docfx.DataContracts.RestApi.pdb
│   │   ├── Docfx.DataContracts.UniversalReference.dll
│   │   ├── Docfx.DataContracts.UniversalReference.pdb
│   │   ├── Docfx.Dotnet.dll
│   │   ├── Docfx.Dotnet.pdb
│   │   ├── Docfx.Glob.dll
│   │   ├── Docfx.Glob.pdb
│   │   ├── Docfx.MarkdigEngine.Extensions.dll
│   │   ├── Docfx.MarkdigEngine.Extensions.pdb
│   │   ├── Docfx.MarkdigEngine.dll
│   │   ├── Docfx.MarkdigEngine.pdb
│   │   ├── Docfx.Plugins.dll
│   │   ├── Docfx.Plugins.pdb
│   │   ├── Docfx.YamlSerialization.dll
│   │   ├── Docfx.YamlSerialization.pdb
│   │   ├── HtmlAgilityPack.dll
│   │   ├── Humanizer.dll
│   │   ├── ICSharpCode.Decompiler.dll
│   │   ├── Jint.dll
│   │   ├── Json.More.dll
│   │   ├── JsonPointer.Net.dll
│   │   ├── JsonSchema.Net.dll
│   │   ├── Markdig.dll
│   │   ├── Microsoft.AspNetCore.Antiforgery.dll
│   │   ├── Microsoft.AspNetCore.Authentication.Abstractions.dll
│   │   ├── Microsoft.AspNetCore.Authentication.BearerToken.dll
│   │   ├── Microsoft.AspNetCore.Authentication.Cookies.dll
│   │   ├── Microsoft.AspNetCore.Authentication.Core.dll
│   │   ├── Microsoft.AspNetCore.Authentication.OAuth.dll
│   │   ├── Microsoft.AspNetCore.Authentication.dll
│   │   ├── Microsoft.AspNetCore.Authorization.Policy.dll
│   │   ├── Microsoft.AspNetCore.Authorization.dll
│   │   ├── Microsoft.AspNetCore.Components.Authorization.dll
│   │   ├── Microsoft.AspNetCore.Components.Endpoints.dll
│   │   ├── Microsoft.AspNetCore.Components.Forms.dll
│   │   ├── Microsoft.AspNetCore.Components.Server.dll
│   │   ├── Microsoft.AspNetCore.Components.Web.dll
│   │   ├── Microsoft.AspNetCore.Components.dll
│   │   ├── Microsoft.AspNetCore.Connections.Abstractions.dll
│   │   ├── Microsoft.AspNetCore.CookiePolicy.dll
│   │   ├── Microsoft.AspNetCore.Cors.dll
│   │   ├── Microsoft.AspNetCore.Cryptography.Internal.dll
│   │   ├── Microsoft.AspNetCore.Cryptography.KeyDerivation.dll
│   │   ├── Microsoft.AspNetCore.DataProtection.Abstractions.dll
│   │   ├── Microsoft.AspNetCore.DataProtection.Extensions.dll
│   │   ├── Microsoft.AspNetCore.DataProtection.dll
│   │   ├── Microsoft.AspNetCore.Diagnostics.Abstractions.dll
│   │   ├── Microsoft.AspNetCore.Diagnostics.HealthChecks.dll
│   │   ├── Microsoft.AspNetCore.Diagnostics.dll
│   │   ├── Microsoft.AspNetCore.HostFiltering.dll
│   │   ├── Microsoft.AspNetCore.Hosting.Abstractions.dll
│   │   ├── Microsoft.AspNetCore.Hosting.Server.Abstractions.dll
│   │   ├── Microsoft.AspNetCore.Hosting.dll
│   │   ├── Microsoft.AspNetCore.Html.Abstractions.dll
│   │   ├── Microsoft.AspNetCore.Http.Abstractions.dll
│   │   ├── Microsoft.AspNetCore.Http.Connections.Common.dll
│   │   ├── Microsoft.AspNetCore.Http.Connections.dll
│   │   ├── Microsoft.AspNetCore.Http.Extensions.dll
│   │   ├── Microsoft.AspNetCore.Http.Features.dll
│   │   ├── Microsoft.AspNetCore.Http.Results.dll
│   │   ├── Microsoft.AspNetCore.Http.dll
│   │   ├── Microsoft.AspNetCore.HttpLogging.dll
│   │   ├── Microsoft.AspNetCore.HttpOverrides.dll
│   │   ├── Microsoft.AspNetCore.HttpsPolicy.dll
│   │   ├── Microsoft.AspNetCore.Identity.dll
│   │   ├── Microsoft.AspNetCore.Localization.Routing.dll
│   │   ├── Microsoft.AspNetCore.Localization.dll
│   │   ├── Microsoft.AspNetCore.Metadata.dll
│   │   ├── Microsoft.AspNetCore.Mvc.Abstractions.dll
│   │   ├── Microsoft.AspNetCore.Mvc.ApiExplorer.dll
│   │   ├── Microsoft.AspNetCore.Mvc.Core.dll
│   │   ├── Microsoft.AspNetCore.Mvc.Cors.dll
│   │   ├── Microsoft.AspNetCore.Mvc.DataAnnotations.dll
│   │   ├── Microsoft.AspNetCore.Mvc.Formatters.Json.dll
│   │   ├── Microsoft.AspNetCore.Mvc.Formatters.Xml.dll
│   │   ├── Microsoft.AspNetCore.Mvc.Localization.dll
│   │   ├── Microsoft.AspNetCore.Mvc.Razor.dll
│   │   ├── Microsoft.AspNetCore.Mvc.RazorPages.dll
│   │   ├── Microsoft.AspNetCore.Mvc.TagHelpers.dll
│   │   ├── Microsoft.AspNetCore.Mvc.ViewFeatures.dll
│   │   ├── Microsoft.AspNetCore.Mvc.dll
│   │   ├── Microsoft.AspNetCore.OutputCaching.dll
│   │   ├── Microsoft.AspNetCore.RateLimiting.dll
│   │   ├── Microsoft.AspNetCore.Razor.Runtime.dll
│   │   ├── Microsoft.AspNetCore.Razor.dll
│   │   ├── Microsoft.AspNetCore.RequestDecompression.dll
│   │   ├── Microsoft.AspNetCore.ResponseCaching.Abstractions.dll
│   │   ├── Microsoft.AspNetCore.ResponseCaching.dll
│   │   ├── Microsoft.AspNetCore.ResponseCompression.dll
│   │   ├── Microsoft.AspNetCore.Rewrite.dll
│   │   ├── Microsoft.AspNetCore.Routing.Abstractions.dll
│   │   ├── Microsoft.AspNetCore.Routing.dll
│   │   ├── Microsoft.AspNetCore.Server.HttpSys.dll
│   │   ├── Microsoft.AspNetCore.Server.IIS.dll
│   │   ├── Microsoft.AspNetCore.Server.IISIntegration.dll
│   │   ├── Microsoft.AspNetCore.Server.Kestrel.Core.dll
│   │   ├── Microsoft.AspNetCore.Server.Kestrel.Transport.NamedPipes.dll
│   │   ├── Microsoft.AspNetCore.Server.Kestrel.Transport.Quic.dll
│   │   ├── Microsoft.AspNetCore.Server.Kestrel.Transport.Sockets.dll
│   │   ├── Microsoft.AspNetCore.Server.Kestrel.dll
│   │   ├── Microsoft.AspNetCore.Session.dll
│   │   ├── Microsoft.AspNetCore.SignalR.Common.dll
│   │   ├── Microsoft.AspNetCore.SignalR.Core.dll
│   │   ├── Microsoft.AspNetCore.SignalR.Protocols.Json.dll
│   │   ├── Microsoft.AspNetCore.SignalR.dll
│   │   ├── Microsoft.AspNetCore.StaticFiles.dll
│   │   ├── Microsoft.AspNetCore.WebSockets.dll
│   │   ├── Microsoft.AspNetCore.WebUtilities.dll
│   │   ├── Microsoft.AspNetCore.dll
│   │   ├── Microsoft.Bcl.AsyncInterfaces.dll
│   │   ├── Microsoft.Build.Framework.dll
│   │   ├── Microsoft.Build.Tasks.Core.dll
│   │   ├── Microsoft.Build.Utilities.Core.dll
│   │   ├── Microsoft.Build.dll
│   │   ├── Microsoft.CSharp.dll
│   │   ├── Microsoft.CodeAnalysis.CSharp.Workspaces.dll
│   │   ├── Microsoft.CodeAnalysis.CSharp.dll
│   │   ├── Microsoft.CodeAnalysis.ExternalAccess.RazorCompiler.dll
│   │   ├── Microsoft.CodeAnalysis.VisualBasic.Workspaces.dll
│   │   ├── Microsoft.CodeAnalysis.VisualBasic.dll
│   │   ├── Microsoft.CodeAnalysis.Workspaces.MSBuild.dll
│   │   ├── Microsoft.CodeAnalysis.Workspaces.dll
│   │   ├── Microsoft.CodeAnalysis.dll
│   │   ├── Microsoft.Extensions.Caching.Abstractions.dll
│   │   ├── Microsoft.Extensions.Caching.Memory.dll
│   │   ├── Microsoft.Extensions.Configuration.Abstractions.dll
│   │   ├── Microsoft.Extensions.Configuration.Binder.dll
│   │   ├── Microsoft.Extensions.Configuration.CommandLine.dll
│   │   ├── Microsoft.Extensions.Configuration.EnvironmentVariables.dll
│   │   ├── Microsoft.Extensions.Configuration.FileExtensions.dll
│   │   ├── Microsoft.Extensions.Configuration.Ini.dll
│   │   ├── Microsoft.Extensions.Configuration.Json.dll
│   │   ├── Microsoft.Extensions.Configuration.KeyPerFile.dll
│   │   ├── Microsoft.Extensions.Configuration.UserSecrets.dll
│   │   ├── Microsoft.Extensions.Configuration.Xml.dll
│   │   ├── Microsoft.Extensions.Configuration.dll
│   │   ├── Microsoft.Extensions.DependencyInjection.Abstractions.dll
│   │   ├── Microsoft.Extensions.DependencyInjection.dll
│   │   ├── Microsoft.Extensions.Diagnostics.Abstractions.dll
│   │   ├── Microsoft.Extensions.Diagnostics.HealthChecks.Abstractions.dll
│   │   ├── Microsoft.Extensions.Diagnostics.HealthChecks.dll
│   │   ├── Microsoft.Extensions.Diagnostics.dll
│   │   ├── Microsoft.Extensions.Features.dll
│   │   ├── Microsoft.Extensions.FileProviders.Abstractions.dll
│   │   ├── Microsoft.Extensions.FileProviders.Composite.dll
│   │   ├── Microsoft.Extensions.FileProviders.Embedded.dll
│   │   ├── Microsoft.Extensions.FileProviders.Physical.dll
│   │   ├── Microsoft.Extensions.FileSystemGlobbing.dll
│   │   ├── Microsoft.Extensions.Hosting.Abstractions.dll
│   │   ├── Microsoft.Extensions.Hosting.dll
│   │   ├── Microsoft.Extensions.Http.dll
│   │   ├── Microsoft.Extensions.Identity.Core.dll
│   │   ├── Microsoft.Extensions.Identity.Stores.dll
│   │   ├── Microsoft.Extensions.Localization.Abstractions.dll
│   │   ├── Microsoft.Extensions.Localization.dll
│   │   ├── Microsoft.Extensions.Logging.Abstractions.dll
│   │   ├── Microsoft.Extensions.Logging.Configuration.dll
│   │   ├── Microsoft.Extensions.Logging.Console.dll
│   │   ├── Microsoft.Extensions.Logging.Debug.dll
│   │   ├── Microsoft.Extensions.Logging.EventLog.dll
│   │   ├── Microsoft.Extensions.Logging.EventSource.dll
│   │   ├── Microsoft.Extensions.Logging.TraceSource.dll
│   │   ├── Microsoft.Extensions.Logging.dll
│   │   ├── Microsoft.Extensions.ObjectPool.dll
│   │   ├── Microsoft.Extensions.Options.ConfigurationExtensions.dll
│   │   ├── Microsoft.Extensions.Options.DataAnnotations.dll
│   │   ├── Microsoft.Extensions.Options.dll
│   │   ├── Microsoft.Extensions.Primitives.dll
│   │   ├── Microsoft.Extensions.WebEncoders.dll
│   │   ├── Microsoft.JSInterop.dll
│   │   ├── Microsoft.NET.StringTools.dll
│   │   ├── Microsoft.Net.Http.Headers.dll
│   │   ├── Microsoft.Playwright.dll
│   │   ├── Microsoft.VisualBasic.Core.dll
│   │   ├── Microsoft.VisualBasic.dll
│   │   ├── Microsoft.VisualStudio.Setup.Configuration.Interop.dll
│   │   ├── Microsoft.Win32.Primitives.dll
│   │   ├── Microsoft.Win32.Registry.dll
│   │   ├── Newtonsoft.Json.dll
│   │   ├── OneOf.dll
│   │   ├── PlantUml.Net.dll
│   │   ├── README.md
│   │   ├── Spectre.Console.Cli.dll
│   │   ├── Spectre.Console.dll
│   │   ├── Stubble.Core.dll
│   │   ├── System.AppContext.dll
│   │   ├── System.Buffers.dll
│   │   ├── System.CodeDom.dll
│   │   ├── System.Collections.Concurrent.dll
│   │   ├── System.Collections.Immutable.dll
│   │   ├── System.Collections.NonGeneric.dll
│   │   ├── System.Collections.Specialized.dll
│   │   ├── System.Collections.dll
│   │   ├── System.ComponentModel.Annotations.dll
│   │   ├── System.ComponentModel.DataAnnotations.dll
│   │   ├── System.ComponentModel.EventBasedAsync.dll
│   │   ├── System.ComponentModel.Primitives.dll
│   │   ├── System.ComponentModel.TypeConverter.dll
│   │   ├── System.ComponentModel.dll
│   │   ├── System.Composition.AttributedModel.dll
│   │   ├── System.Composition.Convention.dll
│   │   ├── System.Composition.Hosting.dll
│   │   ├── System.Composition.Runtime.dll
│   │   ├── System.Composition.TypedParts.dll
│   │   ├── System.Configuration.ConfigurationManager.dll
│   │   ├── System.Configuration.dll
│   │   ├── System.Console.dll
│   │   ├── System.Core.dll
│   │   ├── System.Data.Common.dll
│   │   ├── System.Data.DataSetExtensions.dll
│   │   ├── System.Data.dll
│   │   ├── System.Diagnostics.Contracts.dll
│   │   ├── System.Diagnostics.Debug.dll
│   │   ├── System.Diagnostics.DiagnosticSource.dll
│   │   ├── System.Diagnostics.EventLog.dll
│   │   ├── System.Diagnostics.FileVersionInfo.dll
│   │   ├── System.Diagnostics.Process.dll
│   │   ├── System.Diagnostics.StackTrace.dll
│   │   ├── System.Diagnostics.TextWriterTraceListener.dll
│   │   ├── System.Diagnostics.Tools.dll
│   │   ├── System.Diagnostics.TraceSource.dll
│   │   ├── System.Diagnostics.Tracing.dll
│   │   ├── System.Drawing.Primitives.dll
│   │   ├── System.Drawing.dll
│   │   ├── System.Dynamic.Runtime.dll
│   │   ├── System.Formats.Asn1.dll
│   │   ├── System.Formats.Tar.dll
│   │   ├── System.Globalization.Calendars.dll
│   │   ├── System.Globalization.Extensions.dll
│   │   ├── System.Globalization.dll
│   │   ├── System.IO.Compression.Brotli.dll
│   │   ├── System.IO.Compression.FileSystem.dll
│   │   ├── System.IO.Compression.ZipFile.dll
│   │   ├── System.IO.Compression.dll
│   │   ├── System.IO.FileSystem.AccessControl.dll
│   │   ├── System.IO.FileSystem.DriveInfo.dll
│   │   ├── System.IO.FileSystem.Primitives.dll
│   │   ├── System.IO.FileSystem.Watcher.dll
│   │   ├── System.IO.FileSystem.dll
│   │   ├── System.IO.IsolatedStorage.dll
│   │   ├── System.IO.MemoryMappedFiles.dll
│   │   ├── System.IO.Pipelines.dll
│   │   ├── System.IO.Pipes.AccessControl.dll
│   │   ├── System.IO.Pipes.dll
│   │   ├── System.IO.UnmanagedMemoryStream.dll
│   │   ├── System.IO.dll
│   │   ├── System.Linq.Expressions.dll
│   │   ├── System.Linq.Parallel.dll
│   │   ├── System.Linq.Queryable.dll
│   │   ├── System.Linq.dll
│   │   ├── System.Memory.dll
│   │   ├── System.Net.Http.Json.dll
│   │   ├── System.Net.Http.dll
│   │   ├── System.Net.HttpListener.dll
│   │   ├── System.Net.Mail.dll
│   │   ├── System.Net.NameResolution.dll
│   │   ├── System.Net.NetworkInformation.dll
│   │   ├── System.Net.Ping.dll
│   │   ├── System.Net.Primitives.dll
│   │   ├── System.Net.Quic.dll
│   │   ├── System.Net.Requests.dll
│   │   ├── System.Net.Security.dll
│   │   ├── System.Net.ServicePoint.dll
│   │   ├── System.Net.Sockets.dll
│   │   ├── System.Net.WebClient.dll
│   │   ├── System.Net.WebHeaderCollection.dll
│   │   ├── System.Net.WebProxy.dll
│   │   ├── System.Net.WebSockets.Client.dll
│   │   ├── System.Net.WebSockets.dll
│   │   ├── System.Net.dll
│   │   ├── System.Numerics.Vectors.dll
│   │   ├── System.Numerics.dll
│   │   ├── System.ObjectModel.dll
│   │   ├── System.Private.CoreLib.dll
│   │   ├── System.Private.DataContractSerialization.dll
│   │   ├── System.Private.Uri.dll
│   │   ├── System.Private.Xml.Linq.dll
│   │   ├── System.Private.Xml.dll
│   │   ├── System.Reflection.DispatchProxy.dll
│   │   ├── System.Reflection.Emit.ILGeneration.dll
│   │   ├── System.Reflection.Emit.Lightweight.dll
│   │   ├── System.Reflection.Emit.dll
│   │   ├── System.Reflection.Extensions.dll
│   │   ├── System.Reflection.Metadata.dll
│   │   ├── System.Reflection.MetadataLoadContext.dll
│   │   ├── System.Reflection.Primitives.dll
│   │   ├── System.Reflection.TypeExtensions.dll
│   │   ├── System.Reflection.dll
│   │   ├── System.Resources.Extensions.dll
│   │   ├── System.Resources.Reader.dll
│   │   ├── System.Resources.ResourceManager.dll
│   │   ├── System.Resources.Writer.dll
│   │   ├── System.Runtime.CompilerServices.Unsafe.dll
│   │   ├── System.Runtime.CompilerServices.VisualC.dll
│   │   ├── System.Runtime.Extensions.dll
│   │   ├── System.Runtime.Handles.dll
│   │   ├── System.Runtime.InteropServices.JavaScript.dll
│   │   ├── System.Runtime.InteropServices.RuntimeInformation.dll
│   │   ├── System.Runtime.InteropServices.dll
│   │   ├── System.Runtime.Intrinsics.dll
│   │   ├── System.Runtime.Loader.dll
│   │   ├── System.Runtime.Numerics.dll
│   │   ├── System.Runtime.Serialization.Formatters.dll
│   │   ├── System.Runtime.Serialization.Json.dll
│   │   ├── System.Runtime.Serialization.Primitives.dll
│   │   ├── System.Runtime.Serialization.Xml.dll
│   │   ├── System.Runtime.Serialization.dll
│   │   ├── System.Runtime.dll
│   │   ├── System.Security.AccessControl.dll
│   │   ├── System.Security.Claims.dll
│   │   ├── System.Security.Cryptography.Algorithms.dll
│   │   ├── System.Security.Cryptography.Cng.dll
│   │   ├── System.Security.Cryptography.Csp.dll
│   │   ├── System.Security.Cryptography.Encoding.dll
│   │   ├── System.Security.Cryptography.OpenSsl.dll
│   │   ├── System.Security.Cryptography.Pkcs.dll
│   │   ├── System.Security.Cryptography.Primitives.dll
│   │   ├── System.Security.Cryptography.ProtectedData.dll
│   │   ├── System.Security.Cryptography.X509Certificates.dll
│   │   ├── System.Security.Cryptography.Xml.dll
│   │   ├── System.Security.Cryptography.dll
│   │   ├── System.Security.Permissions.dll
│   │   ├── System.Security.Principal.Windows.dll
│   │   ├── System.Security.Principal.dll
│   │   ├── System.Security.SecureString.dll
│   │   ├── System.Security.dll
│   │   ├── System.ServiceModel.Web.dll
│   │   ├── System.ServiceProcess.dll
│   │   ├── System.Text.Encoding.CodePages.dll
│   │   ├── System.Text.Encoding.Extensions.dll
│   │   ├── System.Text.Encoding.dll
│   │   ├── System.Text.Encodings.Web.dll
│   │   ├── System.Text.Json.dll
│   │   ├── System.Text.RegularExpressions.dll
│   │   ├── System.Threading.Channels.dll
│   │   ├── System.Threading.Overlapped.dll
│   │   ├── System.Threading.RateLimiting.dll
│   │   ├── System.Threading.Tasks.Dataflow.dll
│   │   ├── System.Threading.Tasks.Extensions.dll
│   │   ├── System.Threading.Tasks.Parallel.dll
│   │   ├── System.Threading.Tasks.dll
│   │   ├── System.Threading.Thread.dll
│   │   ├── System.Threading.ThreadPool.dll
│   │   ├── System.Threading.Timer.dll
│   │   ├── System.Threading.dll
│   │   ├── System.Transactions.Local.dll
│   │   ├── System.Transactions.dll
│   │   ├── System.ValueTuple.dll
│   │   ├── System.Web.HttpUtility.dll
│   │   ├── System.Web.dll
│   │   ├── System.Windows.Extensions.dll
│   │   ├── System.Windows.dll
│   │   ├── System.Xml.Linq.dll
│   │   ├── System.Xml.ReaderWriter.dll
│   │   ├── System.Xml.Serialization.dll
│   │   ├── System.Xml.XDocument.dll
│   │   ├── System.Xml.XPath.XDocument.dll
│   │   ├── System.Xml.XPath.dll
│   │   ├── System.Xml.XmlDocument.dll
│   │   ├── System.Xml.XmlSerializer.dll
│   │   ├── System.Xml.dll
│   │   ├── System.dll
│   │   ├── THIRD-PARTY-NOTICES.TXT
│   │   ├── UglyToad.PdfPig.Core.dll
│   │   ├── UglyToad.PdfPig.DocumentLayoutAnalysis.dll
│   │   ├── UglyToad.PdfPig.Fonts.dll
│   │   ├── UglyToad.PdfPig.Package.dll
│   │   ├── UglyToad.PdfPig.Tokenization.dll
│   │   ├── UglyToad.PdfPig.Tokens.dll
│   │   ├── UglyToad.PdfPig.dll
│   │   ├── WindowsBase.dll
│   │   ├── YamlDotNet.dll
│   │   ├── createdump
│   │   ├── docfx
│   │   ├── docfx.deps.json
│   │   ├── docfx.dll
│   │   ├── docfx.pdb
│   │   ├── docfx.runtimeconfig.json
│   │   ├── libSystem.Globalization.Native.so
│   │   ├── libSystem.IO.Compression.Native.so
│   │   ├── libSystem.Native.so
│   │   ├── libSystem.Net.Security.Native.so
│   │   ├── libSystem.Security.Cryptography.Native.OpenSsl.so
│   │   ├── libclrgc.so
│   │   ├── libclrjit.so
│   │   ├── libcoreclr.so
│   │   ├── libcoreclrtraceptprovider.so
│   │   ├── libhostfxr.so
│   │   ├── libhostpolicy.so
│   │   ├── libmscordaccore.so
│   │   ├── libmscordbi.so
│   │   ├── mscorlib.dll
│   │   ├── netstandard.dll
│   │   └── playwright.ps1
│   ├── DOCKER.md
│   ├── README.md
│   ├── STRUCTURE.md
│   ├── TECHNICAL.md
│   ├── build.sh
│   ├── docfx.json
│   └── toc.yml
├── frontend
│   └── static
│       ├── css
│       │   ├── base.css
│       │   ├── buttons.css
│       │   ├── components.css
│       │   ├── footer.css
│       │   ├── header.css
│       │   ├── layout.css
│       │   ├── nav.css
│       │   ├── theme.css
│       │   ├── utilities.css
│       │   └── variables.css
│       ├── js
│       │   └── main.js
│       ├── templates
│       │   ├── auth
│       │   │   ├── dashboard.html
│       │   │   ├── login.html
│       │   │   ├── profile.html
│       │   │   └── register.html
│       │   ├── components
│       │   │   ├── alert.html
│       │   │   ├── breadcrumb.html
│       │   │   ├── card.html
│       │   │   ├── form-input.html
│       │   │   ├── loading.html
│       │   │   └── modal.html
│       │   ├── dialog
│       │   │   ├── alert.html
│       │   │   ├── confirm.html
│       │   │   ├── form.html
│       │   │   ├── loading.html
│       │   │   └── prompt.html
│       │   ├── errors
│       │   │   ├── 400.html
│       │   │   ├── 403.html
│       │   │   ├── 404.html
│       │   │   ├── 500.html
│       │   │   └── maintenance.html
│       │   ├── layouts
│       │   │   ├── admin.html
│       │   │   ├── base.html
│       │   │   ├── clean.html
│       │   │   ├── single-column.html
│       │   │   └── two-column.html
│       │   └── main
│       │       └── index.html
│       ├── favicon.svg
│       └── index.html
├── infrastructure
│   └── docker
│       ├── compose
│       │   ├── overrides
│       │   │   ├── ci-cd.yml
│       │   │   ├── development.yml
│       │   │   ├── edge.yml
│       │   │   ├── production.yml
│       │   │   └── testing.yml
│       │   ├── services
│       │   │   ├── adminer.yml
│       │   │   ├── backend.yml
│       │   │   ├── database.yml
│       │   │   └── frontend.yml
│       │   └── shared
│       │       ├── environment.env
│       │       ├── networks.yml
│       │       ├── secrets.yml
│       │       └── volumes.yml
│       ├── database-init
│       │   └── 01-init-database.sql
│       ├── dockerfiles
│       │   ├── Dockerfile.development
│       │   ├── Dockerfile.multi-stage
│       │   └── Dockerfile.production
│       ├── scripts
│       │   ├── entrypoints
│       │   │   ├── entrypoint-dev.sh
│       │   │   └── entrypoint-prod.sh
│       │   ├── compose.sh
│       │   └── test-infrastructure.sh
│       ├── .env
│       └── docker-compose.yml
├── scripts
│   ├── compile-bytecode.ps1
│   └── compile-bytecode.sh
├── src
│   ├── goldilocks
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── main.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   └── app_factory.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   └── forms.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   └── auth.py
│   │   ├── tests
│   │   │   ├── api
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_api_endpoints.py
│   │   │   │   └── test_auth_endpoints.py
│   │   │   ├── core
│   │   │   │   ├── __init__.py
│   │   │   │   └── test_app_factory.py
│   │   │   ├── errors
│   │   │   │   ├── __init__.py
│   │   │   │   └── test_404.py
│   │   │   ├── health
│   │   │   │   ├── __init__.py
│   │   │   │   └── test_health.py
│   │   │   ├── index
│   │   │   │   ├── version
│   │   │   │   └── test_index.py
│   │   │   ├── models
│   │   │   │   ├── __init__.py
│   │   │   │   └── test_database_models.py
│   │   │   ├── services
│   │   │   │   ├── __init__.py
│   │   │   │   └── test_auth_service.py
│   │   │   ├── templates
│   │   │   │   ├── __init__.py
│   │   │   │   └── test_template_system.py
│   │   │   ├── utils
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_helpers.py
│   │   │   │   └── test_utils.py
│   │   │   ├── version
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_version.py
│   │   │   │   └── test_version_fallback.py
│   │   │   ├── __init__.py
│   │   │   └── conftest.py
│   │   ├── utils
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   └── app.py
│   └── instance
│       └── goldilocks.db
├── .env
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── AGENT.md
├── Dockerfile
├── Makefile
├── README.md
├── app.py
├── clean.py
├── docker-bake.json
├── package-lock.json
├── package.json
├── pyproject.toml
├── requirements.txt
└── start-dev.sh
```

## File Organization Principles

### Configuration Files (`config/`)

- All tool configurations are centralized here
- Original files are kept in config/, with copies in root only when required by tools
- Examples: pytest, mypy, flake8, cypress, pre-commit

### Documentation (`docs/`)

- All project documentation
- README.md is copied to root for GitHub compatibility
- Technical specifications and development guides
- Automated build system with DocFX

### Infrastructure (`infrastructure/`)

- Container definitions (multi-stage Dockerfiles)
- Deployment configurations
- Environment-specific setups

### Docker Scripts (`infrastructure/docker/scripts/`)

- Build automation and management scripts
- Development utilities and testing
- Container deployment management
- Linux-based DevContainer environment

### Source Code (`src/`)

- All Python source code in `src/goldilocks/`
- Tests are in `src/goldilocks/tests/`
- Follows Python src layout best practices

## Quick Start

1. **Development**: Use the optimized devcontainer or Docker compose
2. **Testing**: `python -m pytest` (uses config/pyproject.toml)
3. **E2E Tests**: `npm run test:e2e` (uses config/cypress.config.js)
4. **Build**: Use scripts in `scripts/` directory
5. **Deploy**: Use configurations in `infrastructure/`

For detailed information, see [docs/README.md](docs/README.md).
