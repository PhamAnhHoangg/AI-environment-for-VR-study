using System;
using System.IO;
using UnityEngine;

/// <summary>
/// AIOutputPaths — one place that decides where the Python AI tools save images.
///
/// Resolution order:
///   1. The AI_OUTPUT_DIR environment variable (the Python tools read the same one).
///      Set it before starting Unity Hub / the Editor, or Unity will not see it.
///   2. Otherwise: "ai_output" next to the Assets folder of this Unity project,
///      which matches the Python default of &lt;UNITY_PROJECT_DIR&gt;/ai_output.
///
/// Call from Start() or Awake() (Application.dataPath is main-thread only).
/// </summary>
public static class AIOutputPaths
{
    public static string Dir
    {
        get
        {
            string env = Environment.GetEnvironmentVariable("AI_OUTPUT_DIR");
            if (!string.IsNullOrEmpty(env)) return env;
            return Path.GetFullPath(Path.Combine(Application.dataPath, "..", "ai_output"));
        }
    }

    /// <summary>Returns <paramref name="configured"/> if set, else AI output dir + fileName.</summary>
    public static string Resolve(string configured, string fileName)
    {
        return string.IsNullOrEmpty(configured) ? Path.Combine(Dir, fileName) : configured;
    }
}
