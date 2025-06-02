using System.Diagnostics;
using LinkedList;

namespace good_morning_espanso_package;

class Program
{
    static void Main(string[] args)
    {
        char tagChar = ':';
        string resourcesFolder = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "resources"),
               namesFile = Path.Combine(resourcesFolder, "names.txt"),
               personalFile = Path.Combine(resourcesFolder, "personal.txt"),
               generalFile = Path.Combine(resourcesFolder, "general.txt"),
               mondaysFile = Path.Combine(resourcesFolder, "mondays.txt"),
               fridaysFile = Path.Combine(resourcesFolder, "fridays.txt");

        Random random = new Random();
        System.Diagnostics.Process process = new Process()
        {
            StartInfo = new ProcessStartInfo()
            {
                FileName = "cmd.exe",
                Arguments = "/C curl -o /resources/tmp.png ",
                WindowStyle = ProcessWindowStyle.Hidden

            }

        };

        List<string> personalGreetings = new List<string>(),
                     generalGreetings = new List<string>(),
                     mondayGreetings = new List<string>(),
                     fridayGreetings = new List<string>();
        DoublyLinkedList<string> shuffle = new DoublyLinkedList<string>(),
                                 output = new DoublyLinkedList<string>();

        foreach (string greeting in File.ReadAllLines(personalFile))
            personalGreetings.Add(greeting);

        foreach (string greeting in File.ReadAllLines(generalFile))
            generalGreetings.Add(greeting);

        foreach (string greeting in File.ReadAllLines(mondaysFile))
            mondayGreetings.Add(greeting);

        foreach (string greeting in File.ReadAllLines(fridaysFile))
            fridayGreetings.Add(greeting);

        foreach (string name in File.ReadAllLines(namesFile))
        {
            /* If the name is tagged, add it directly to the output in the order it appears in the original file. Otherwise, either append or prepend
             *  the name to the names list depending on whether a random value between 0 and 99 is even or odd. This builds the list in a semi-random 
             *  order and prevents the need to shuffle the values later on.*/
            if (name.Contains(tagChar))
                output.Append(name.Substring(name.IndexOf(tagChar) + 1));
            else if (random.Next(0, 99) % 2 == 0)
                shuffle.Append(name);
            else
                shuffle.Prepend(name);

        }

        if (shuffle.First is not null)
            output.Append(shuffle.First); // If shuffle contains any nodes, link the first node of shuffle to the output list.

        foreach (string name in output)
            Console.WriteLine($"{personalGreetings[random.Next(0, personalGreetings.Count - 1)]} {name}!");

        if (DateTime.Today.DayOfWeek == DayOfWeek.Monday)
            Console.WriteLine($"\n{mondayGreetings[random.Next(0, mondayGreetings.Count - 1)]}");
        else if (DateTime.Today.DayOfWeek == DayOfWeek.Friday)
            Console.WriteLine($"\n{fridayGreetings[random.Next(0, fridayGreetings.Count - 1)]}");
        else
            Console.WriteLine($"\n{generalGreetings[random.Next(0, generalGreetings.Count - 1)]}");

    }

}

