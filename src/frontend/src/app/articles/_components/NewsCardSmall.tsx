import classes from "./NewsCardSmall.module.css";
import { Avatar, Card, Group, Image, Text, Badge } from "@mantine/core";

const stats = [
  { value: 447, label: "Remaining" },
  { value: 76, label: "In progress" },
];

type CardData = {
  uuid: string;
  title: string;
  description: string;
  snippet: string;
  url: string;
  image_url: string;
  published_at: string;
  source: string;
  categories: string[];
};

// export default function NewsCardSmall(props: { data: CardData }) {
//   const items = stats.map((stat) => (
//     <div key={stat.label}>
//       <Text className={classes.label}>{stat.value}</Text>
//       <Text size="xs" c="dimmed">
//         {stat.label}
//       </Text>
//     </div>
//   ));

//   return (
//     <Card shadow="sm" padding="lg" radius="md" withBorder>
//       <Card.Section>
//         <Image
//           src="https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/images/bg-8.png"
//           height={160}
//           alt="Norway"
//         />
//       </Card.Section>

//       <Group justify="space-between" mt="md" mb="xs">
//         <Text fw={500}>Norway Fjord Adventures</Text>
//         <Badge color="pink">On Sale</Badge>
//       </Group>

//       <Text size="sm" c="dimmed">
//         With Fjord Tours you can explore more of the magical fjord landscapes
//         with tours and activities on and around the fjords of Norway
//       </Text>
//     </Card>
//   );
// }

export default function NewsCardSmall(props: { data: CardData }) {
  return (
    <Card withBorder radius="md" p={0} className={classes.card}>
      <Group wrap="nowrap" gap={0}>
        <Image
          src="https://images.unsplash.com/photo-1602080858428-57174f9431cf?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=400&q=80"
          height={160}
        />
        <div className={classes.body}>
          <Text tt="uppercase" c="dimmed" fw={700} size="xs">
            technology
          </Text>
          <Text className={classes.title} mt="xs" mb="md">
            The best laptop for Frontend engineers in 2022
          </Text>
          <Group wrap="nowrap" gap="xs">
            <Group gap="xs" wrap="nowrap">
              <Avatar
                size={20}
                src="https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-8.png"
              />
              <Text size="xs">Elsa Typechecker</Text>
            </Group>
            <Text size="xs" c="dimmed">
              •
            </Text>
            <Text size="xs" c="dimmed">
              Feb 6th
            </Text>
          </Group>
        </div>
      </Group>
    </Card>
  );
}
